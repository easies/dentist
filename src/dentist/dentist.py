import re
import pwd
import logging
import select
import time
import fcntl
import signal
import os


class Poller(object):

    def __init__(self):
        self.poller = select.poll()
        self.all = {}

    def register_file_watcher(self, fw):
        self.poller.register(fw.file, select.POLLIN)
        self.all[fw.file.fileno()] = fw

    def unregister(self, fw):
        try:
            self.poller.unregister(fw.file)
            del self.all[fw.file.fileno()]
        except KeyError:
            # ignore fd's that weren't registered in the first place.
            pass

    def poll(self):
        try:
            for fd, event in self.poller.poll():
                if event & select.POLLIN:
                    logging.debug('ready for %d' % fd)
                    self.all[fd].read_line()
        except select.error, e:
            if e[0] != 4:
                raise


class DirWatcher(object):
    signal_registered = False

    def __init__(self, paths, fws=None):
        if not self.__class__.signal_registered:
            self.__class__.signal_registered = True
            signal.signal(signal.SIGIO, self.handler)

        self.directories = []

        # Watch all given directories for changes.
        for path in paths:
            d = os.open(path, os.O_RDONLY)
            self.directories.append(d)
            fcntl.fcntl(d, fcntl.F_SETSIG, 0)
            fcntl.fcntl(d, fcntl.F_NOTIFY,
                        (fcntl.DN_MODIFY | fcntl.DN_DELETE | fcntl.DN_RENAME |
                         fcntl.DN_CREATE | fcntl.DN_MULTISHOT))

        if fws is not None:
            self.fws = fws
        else:
            self.fws = []

    def add_file_watcher(self, fw):
        self.fws.append(fw)

    def handler(self, signum, frame):
        logging.debug('A file changed.')
        # XXX queue this action
        for fw in self.fws:
            fw.check()


class FileWatcher(object):

    def __init__(self, path, reader, poller):
        self.path = os.path.abspath(path)
        self.enabled = True
        try:
            self.file = open(self.path, 'rb')
        except IOError:
            self.file = None
            self.enabled = False
        self.reader = reader
        self.last = 0
        self.current = 0
        self.poller = poller
        self.check()
        if self.enabled:
            self.poller.register_file_watcher(self)

    def read_line(self):
        if not self.enabled:
            return
        self.last = self.current
        line = self.file.readline()
        self.current = self.file.tell()

        logging.debug('%d %d' % (self.last, self.current))

        if not line or self.current == self.last:
            # EOF
            logging.debug('EOF encountered, disabling.')
            self.enabled = False
            self.poller.unregister(self)
            return

        logging.debug('line: %s' % line.strip())

        user = self.reader.check_line(line)
        if user:
            self.write_to_user(user, line, self.path)

    def write_to_user(self, user, line, path):
        logging.debug('Writing to %s : %s' % (user.pw_name, line))
        dir_name = os.path.dirname(path)
        basename = os.path.basename(path)
        userpath = os.path.join(dir_name, '%s_%s' % (user.pw_name, basename))
        
        # XXX cache/poll the open files?
        open(userpath, 'a').write(line)
        
        logging.debug('Written to %s' % user.pw_name)

    def disable(self):
        try:
            self.file.close()
        except (OSError, AttributeError):
            pass
        self.file = None
        self.current = 0
        self.last = 0
        self.enabled = False

    def enable(self):
        self.file = open(self.path, 'rb')
        self.poller.register_file_watcher(self)
        self.current = 0
        self.last = 0
        self.enabled = True

    def check(self):
        try:
            # Check if the file exists.
            st = os.stat(self.path)
        except OSError:
            # The file does not exist, disable.
            self.disable()
            return

        if self.file is None:
            logging.debug('New file %s, enabling.' % self.path)
            self.enable()
            return

        if st.st_size < self.last:
            logging.debug('File %s shrunk, rewinding.' % self.path)
            self.current = 0
            self.last = 0

        self.file.seek(self.current)

        if not self.enabled:
            self.poller.register_file_watcher(self)
            self.enabled = True


class LogReader(object):
    output_directory = '/tmp'

    @classmethod
    def set_output_directory(cls, path):
        cls.output_directory = path

    @classmethod
    def get_info(cls, user):
        """
        >>> pwd.getpwnam('root') is not None
        True
        """
        try:
            return pwd.getpwnam(user)
        except KeyError:
            return None

    @classmethod
    def check_line(cls, line):
        raise NotImplementedError


class CombinedLogReader(LogReader):
    """Parse Apache logs in the combined format.
    "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-agent}i\\"
    """

    # 1 = Remote host
    # 2 = remote ident
    # 3 = ?
    # 4 = date
    # 5 = HTTP Request, (GET, POST, etc.)
    # 6 = URI
    # 7 = HTTP version
    # 8 = Rest
    REGEX = (r'^([^ ]+) ([^ ]+) ([^ ]+) \[([^]]+)\] '
             r'"([^ ]+) ([^ ]+) ([^ ]+)" ?(.*)$')
    REGEX_C = re.compile(REGEX)
    prefixes = ['/~']

    @classmethod
    def add_prefix(cls, *args):
        """
        >>> cls = CombinedLogReader
        >>> '/~' in cls.prefixes
        True
        >>> cls.add_prefix('abc', 'xyz')
        >>> 'abc' in cls.prefixes
        True
        >>> 'xyz' in cls.prefixes
        True
        """
        cls.prefixes += args

    @classmethod
    def check_line(cls, line):
        uri = cls.parse_uri(line)
        if uri is not None:
           user = cls.parse_user(uri)
           if user is not None:
               return cls.get_info(user)

    @classmethod
    def parse_uri(cls, line):
        m = cls.REGEX_C.match(line)
        if m is not None:
            uri = m.group(6)
            return uri

    @classmethod
    def parse_user(cls, uri):
        """
        >>> clr = CombinedLogReader()
        >>> clr.parse_user('')
        >>> clr.parse_user('/')
        >>> clr.parse_user('/otherstuff')
        >>> clr.parse_user('/~abc')
        'abc'
        >>> clr.parse_user('/~abc/index.html')
        'abc'
        >>> clr.parse_user('/home/abc')
        >>> clr.parse_user('/home/abc/index.html')
        >>> clr.add_prefix('/home/')
        >>> clr.parse_user('/home/abc')
        'abc'
        >>> clr.parse_user('/home/abc/index.html')
        'abc'
        """
        for p in cls.prefixes:
            if uri.startswith(p):
                s = uri[len(p):]
                return s.split('/', 1)[0]


class ErrorLogReader(LogReader):
    HOMEDIR_ROOT = '/home'
    HOMEDIR_ROOT_LEN = len(HOMEDIR_ROOT)

    @classmethod
    def configure(cls, **kwargs):
        """
        >>> ErrorLogReader.HOMEDIR_ROOT
        '/home'
        >>> ErrorLogReader.configure()
        >>> ErrorLogReader.HOMEDIR_ROOT
        '/home'
        >>> ErrorLogReader.configure(homedir_root='/other/home')
        >>> ErrorLogReader.HOMEDIR_ROOT
        '/other/home'
        """
        try:
            cls.HOMEDIR_ROOT = kwargs['homedir_root']
            cls.HOMEDIR_ROOT_LEN = len(cls.HOMEDIR_ROOT)
        except KeyError:
            pass

    @classmethod
    def check_line(cls, line):
        index = line.find(HOMEDIR_ROOT)
        if index < 0:
            return

        index += HOMEDIR_ROOT_LEN
        user = line[index:].split('/', 1)[0].split(' ')[0]
        return cls.get_info(user)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
