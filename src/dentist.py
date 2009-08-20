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
        fw.poller = self

    def unregister(self, fw):
        del self.all[fw.file.fileno()]
        self.poller.unregister(fw.file)

    def poll(self):
        try:
            for fd, event in self.poller.poll():
                if event & select.POLLIN:
                    self.all[fd].read_line()
        except:
            pass


class DirWatcher(object):
    signal_registered = False

    def __init__(self, path, fws):
        if not self.__class__.signal_registered:
            self.__class__.signal_registered = True
            signal.signal(signal.SIGIO, self.handler)

        self.dir = os.open(path, os.O_RDONLY)
        fcntl.fcntl(self.dir, fcntl.F_SETSIG, 0)
        fcntl.fcntl(self.dir, fcntl.F_NOTIFY,
                    fcntl.DN_MODIFY | fcntl.DN_MULTISHOT)
        self.fws = fws

    def handler(self, signum, frame):
        logging.debug(frame)
        logging.debug(dir(frame))
        logging.debug(signum)

        # XXX queue this action
        for fw in self.fws:
            if not fw.enabled:
                fw.reenable()


class FileWatcher(object):

    def __init__(self, path, reader):
        self.file = open(path, 'rb')
        self.reader = reader
        self.last = 0
        self.enabled = True
        self.poller = None

    def read_line(self):
        if not self.enabled:
            return
        self.last = self.file.tell()
        line = self.file.readline()
        if not line:
            self.enabled = False
            self.poller.unregister(self)
#            time.sleep(0.1)
#            self.file.seek(0, os.SEEK_END)
            return

        logging.debug(line)

        user = self.reader.check_line(line)
        if user is not None:
            self.write_to_user(user, line)

    def write_to_user(self, user, line):
        #logging.debug('Writing to %s : %s' % (user, line))
        pass
    
    def reenable(self):
        self.enabled = True
        st = os.fstat(self.file.fileno())
        if st.st_size < self.last:
            self.last = 0
        self.file.seek(self.last)
        self.poller.register_file_watcher(self)


class CombinedLogReader(object):
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
    REGEX = r'^([^ ]+) ([^ ]+) ([^ ]+) \[([^]]+)\] "([^ ]+) ([^ ]+) ([^ ]+)" ?(.*)$'
    REGEX_C = re.compile(REGEX)

    @classmethod
    def check_line(cls, line):
        uri = cls.parse_uri(line)
        if uri is not None:
           user = cls.parse_user(uri)
           if user is not None:
               if cls.user_exists(user):
                   return user

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
        >>> clr.parse_user('/home/abc')
        'abc'
        >>> clr.parse_user('/home/abc/index.html')
        'abc'
        >>> clr.parse_user('/~abc')
        'abc'
        >>> clr.parse_user('/~abc/index.html')
        'abc'
        >>> clr.parse_user('/')
        >>> clr.parse_user('/otherstuff')
        """
        if uri.startswith('/home/'):
            user = uri.split('/', 3)[2]
            return user
        if uri.startswith('/~'):
            x = uri.split('~', 1)[1]
            y = x.split('/', 1)
            return y[0]

    @classmethod
    def user_exists(cls, user):
        try:
            pwent = pwd.getpwnam(user)
            return True
        except KeyError:
            return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
