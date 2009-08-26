import os
import fcntl
import select
import logging
import inotify
from inotify import IN_DELETE_SELF, IN_MODIFY, IN_CREATE

class Poller(object):
    """Watch file descriptors using poll(2) (read-only)."""

    def __init__(self):
        """Create a polling object and that keeps track."""
        self.poller = select.poll()
        self.all = {}

    def register(self, fd, callback):
        self.poller.register(fd, select.POLLIN)
        self.all[fd] = callback

    def unregister(self, fd):
        try:
            self.poller.unregister(fd)
            del self.all[fd]
        except KeyError:
            # ignore fd's that weren't registered in the first place.
            pass

    def poll(self):
        for fd, event in self.poller.poll():
            if event & select.POLLIN:
                logging.debug('ready for %d' % fd)
                self.all[fd]()


class Notifier(object):

    def __init__(self):
        self.inotify = inotify.Inotify()
        self.all = {}

    def add_log_notify(self, ln):
        wd = self.inotify.add_watch(ln.path,
                                    IN_DELETE_SELF | IN_MODIFY | IN_CREATE)
        self.all[wd] = ln.handler

    def handler(self):
        self.inotify.read_into_buffer()
        event = self.inotify.get_event()
        if event:
            self.all[event.wd](event)


class LogNotify(object):

    def __init__(self, path, reader):
        self.path = os.path.abspath(path)
        self.reader = reader
        try:
            st = os.stat(self.path)
            self.file = open(self.path, 'rb')
        except OSError:
            self.file = None
            return
        self.file.seek(st.st_size)
        self.last = st.st_size

    def output_file(self, user):
        d = self.reader.output_directory
        f = '%s_%s' % (user.pw_name, os.path.basename(self.path))
        return os.path.join(d, f)

    def in_delete(self):
        self.file.close()
        self.last = 0

    def in_modify(self):
        st = os.stat(self.path)
        while self.last < st.st_size:
            line = self.file.readline()
            user = self.reader.check_line(line)
            if user:
                output = self.output_file(user)
                open(output, 'a').write(line)
                os.chmod(output, 400)
                os.chown(output, user.pw_uid, user.pw_gid)
            self.last += len(line)

    def in_create(self):
        self.file = open(self.path, 'rb')
        self.last = 0

    def handler(self, event):
        logging.debug(event)
        if event.mask & inotify.IN_DELETE_SELF:
            self.in_delete()
        elif event.mask & inotify.IN_MODIFY:
            self.in_modify()
        elif event.mask & inotify.IN_CREATE:
            self.in_create()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
