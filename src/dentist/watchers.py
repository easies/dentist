import os
import fcntl
import select
import logging


class Poller(object):
    """Watches file descriptors using poll(2)"""

    def __init__(self):
        """Create a polling object and that keeps track."""
        self.poller = select.poll()
        self.all = {}

    def register(self, fw):
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
            # poll(2) was interrupted because of SIGIO
            if e[0] != 4:
                raise


class DirWatcher(object):
    signal_registered = False

    def __init__(self, paths, fws=None):
        import signal
        if not self.__class__.signal_registered:
            self.__class__.signal_registered = True
            signal.signal(signal.SIGIO, self.handler)

        self.directories = []

        # Watch all given directories for changes.
        for path in paths:
            d = os.open(path, os.O_RDONLY)
            self.directories.append(d)
            fcntl.fcntl(d, fcntl.F_SETSIG, signal.SIGIO)
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
        self.reader = reader
        self.poller = poller
        self.path = os.path.abspath(path)
        self.enabled = False
        try:
            self.file = open(self.path, 'rb')
            st = os.fstat(self.file.fileno())
            self.last = st.st_size
            self.current = st.st_size
            # Start from the end.
        except IOError:
            self.file = None
            self.last = 0
            self.current = 0
            # The file does not exist yet.

        self.check()

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
        self.poller.register(self)
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
            # The file previously did not exist.
            logging.debug('New file %s, enabling.' % self.path)
            self.enable()
            return

        if st.st_size < self.current:
            # The size of the file shrunk from the last place we read.
            logging.debug('File %s shrunk, rewinding.' % self.path)
            self.current = 0
            self.last = 0

        self.file.seek(self.current)

        if not self.enabled:
            self.poller.register(self)
            self.enabled = True


if __name__ == '__main__':
    import doctest
    doctest.testmod()
