"""Wrapper for inotify(7)"""

import _inotify
import struct
import os
import fcntl
import termios
import array


# Some flags
IN_ACCESS = _inotify.IN_ACCESS
IN_MODIFY = _inotify.IN_MODIFY
IN_ATTRIB = _inotify.IN_ATTRIB
IN_CLOSE_WRITE = _inotify.IN_CLOSE_WRITE
IN_CLOSE_NOWRITE = _inotify.IN_CLOSE_NOWRITE
IN_OPEN = _inotify.IN_OPEN
IN_MOVED_FROM = _inotify.IN_MOVED_FROM
IN_MOVED_TO = _inotify.IN_MOVED_TO
IN_CREATE = _inotify.IN_CREATE
IN_DELETE = _inotify.IN_DELETE
IN_DELETE_SELF = _inotify.IN_DELETE_SELF
IN_MOVE_SELF = _inotify.IN_MOVE_SELF
IN_UNMOUNT = _inotify.IN_UNMOUNT
IN_Q_OVERFLOW = _inotify.IN_Q_OVERFLOW
IN_IGNORED = _inotify.IN_IGNORED
IN_CLOSE = _inotify.IN_CLOSE
IN_MOVE = _inotify.IN_MOVE
IN_ONLYDIR = _inotify.IN_ONLYDIR
IN_DONT_FOLLOW = _inotify.IN_DONT_FOLLOW
IN_MASK_ADD = _inotify.IN_MASK_ADD
IN_ISDIR = _inotify.IN_ISDIR
IN_ONESHOT = _inotify.IN_ONESHOT
IN_ALL_EVENTS = _inotify.IN_ALL_EVENTS


class Watch(object):

    def __init__(self, path, notify):
        self.path = path
        self.notify = notify
        self.wd = -1
        self.callbacks = {}

    def add_callback(self, mask, callback):
        self.callbacks[mask] = callback
        return self


class Inotify(object):

    def __init__(self):
        self.__fd = _inotify.init()
        self.__buffer = ''

    def __getattr__(self, name):
        """
        >>> x = Inotify()
        >>> x.buffer
        ''
        """
        if name == 'buffer':
            return self.__buffer
        raise AttributeError

    def fileno(self):
        """
        @return the file descriptor of this Inotify object.
        """
        return self.__fd

    def add_watch(self, path, mask):
        return _inotify.add_watch(self.__fd, path, mask)

    def rm_watch(self, wd):
        return _inotify.rm_watch(self.__fd, wd)

    def read_into_buffer(self):
        self.__buffer += os.read(self.__fd, 4096)

    def get_event(self):
        """
        >>> import tempfile
        >>> import time
        >>> temp_d = tempfile.mkdtemp()
        >>> x = Inotify()
        >>> x.get_event()
        >>> x.add_watch(temp_d, IN_CREATE)
        1
        >>> temp_f = tempfile.TemporaryFile(dir=temp_d)
        >>> time.sleep(0.1)
        >>> x.read_into_buffer()
        >>> e = x.get_event()
        >>> e.wd
        1
        >>> os.rmdir(temp_d)
        """
        # struct inotify_event {
        #   int wd;
        #   uint32_t mask;
        #   uint32_t cookie;
        #   uint32_t len;
        #   char * name; };
        buffer_len = len(self.__buffer)
        if buffer_len < 16:
            return
        wd, mask, cookie, length = struct.unpack('iIII', self.__buffer[0:16])

        if 16 + length <= buffer_len:
            name = self.__buffer[16:16+length].rstrip('\0')
            self.__buffer = self.__buffer[16+length:]
            return Event(wd, mask, cookie, name)


class Event(object):
    """An Event object.
    >>> e = Event(1, 1, 1, 'abc')
    >>> e.wd == 1
    True
    >>> e.mask == 1
    True
    >>> e.cookie == 1
    True
    >>> e.name == 'abc'
    True
    """

    def __init__(self, wd, mask, cookie, name):
        self.__wd = wd
        self.mask = mask
        self.cookie = cookie
        self.name = name

    def __getattr__(self, name):
        """
        >>> x = Event(1, 2, 3, 'hello')
        >>> x.wd
        1
        """
        if name == 'wd':
            return self.__wd
        raise AttributeError

    def __str__(self):
        """
        >>> x = Event(1, 2, 3, 'hello')
        >>> str(x)
        '1 2 3 hello'
        """
        return '%d %d %d %s' % (self.__wd, self.mask, self.cookie, self.name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
