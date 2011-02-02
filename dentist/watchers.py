import os
import fcntl
import select
import logging
import inotify
from inotify import IN_DELETE, IN_MODIFY, IN_CREATE, IN_ALL_EVENTS

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
        self.all_directories = {}

    def add_log_notify(self, ln):
        dir_name = os.path.dirname(ln.path)
        base_name = os.path.basename(ln.path)
        if not dir_name in self.all_directories.keys():
            wd = self.inotify.add_watch(dir_name, ln.__class__.MASK)
            self.all_directories[dir_name] = wd
        else:
            wd = self.all_directories[dir_name]
        self.all[(wd, base_name)] = ln.handler

    def handler(self):
        self.inotify.read_into_buffer()
        event = self.inotify.get_event()
        logging.debug(event)
        if event:
            try:
                self.all[(event.wd, event.name)](event)
            except KeyError:
                pass


class LogNotify(object):
    MASK = IN_DELETE | IN_MODIFY | IN_CREATE

    def __init__(self, path, reader):
        self.path = os.path.abspath(path)
        self.reader = reader
        try:
            st = os.stat(self.path)
            self.file = open(self.path, 'rb')
        except OSError:
            self.file = None
            self.last = 0
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
        if self.last > st.st_size:
            # The file shrunk, re-add
            self.in_delete()
            self.in_create()
        while self.last < st.st_size:
            line = self.file.readline()
            user = self.reader.check_line(line)
            if user:
                logging.debug('%s : writing to user.' % user.pw_name)
                output = self.output_file(user)
                open(output, 'a').write(line)
                logging.debug('%s : wrote to user : %s ...' % 
                              (user.pw_name, line[:50]))
                os.chmod(output, 0400)
                os.chown(output, user.pw_uid, user.pw_gid)
            self.last += len(line)

    def in_create(self):
        self.file = open(self.path, 'rb')
        self.last = 0

    def handler(self, event):
        if event.mask & inotify.IN_DELETE:
            logging.debug('%s deleted.' % self.path)
            self.in_delete()
        elif event.mask & inotify.IN_MODIFY:
            logging.debug('%s modified.' % self.path)
            self.in_modify()
        elif event.mask & inotify.IN_CREATE:
            logging.debug('%s created.' % self.path)
            self.in_create()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
