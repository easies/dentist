cdef extern from "unistd.h":
    ctypedef unsigned int size_t
    ctypedef int ssize_t
    ctypedef unsigned int uint32_t
    ssize_t read(int fd, void *buf, size_t nbytes)


cdef extern from "sys/inotify.h":
    struct inotify_event
    int C_IN_ACCESS "IN_ACCESS"
    int C_IN_MODIFY "IN_MODIFY"
    int C_IN_ATTRIB "IN_ATTRIB"
    int C_IN_CLOSE_WRITE "IN_CLOSE_WRITE"
    int C_IN_CLOSE_NOWRITE "IN_CLOSE_NOWRITE"
    int C_IN_OPEN "IN_OPEN"
    int C_IN_MOVED_FROM "IN_MOVED_FROM"
    int C_IN_MOVED_TO "IN_MOVED_TO"
    int C_IN_CREATE "IN_CREATE"
    int C_IN_DELETE "IN_DELETE"
    int C_IN_DELETE_SELF "IN_DELETE_SELF"
    int C_IN_MOVE_SELF "IN_MOVE_SELF"
    int C_IN_UNMOUNT "IN_UNMOUNT"
    int C_IN_Q_OVERFLOW "IN_Q_OVERFLOW"
    int C_IN_IGNORED "IN_IGNORED"
    int C_IN_CLOSE "IN_CLOSE"
    int C_IN_MOVE "IN_MOVE"
    int C_IN_ONLYDIR "IN_ONLYDIR"
    int C_IN_DONT_FOLLOW "IN_DONT_FOLLOW"
    int C_IN_MASK_ADD "IN_MASK_ADD"
    int C_IN_ISDIR "IN_ISDIR"
    int C_IN_ONESHOT "IN_ONESHOT"
    int C_IN_ALL_EVENTS "IN_ALL_EVENTS"
    int inotify_init()
    int inotify_add_watch(int, char *, uint32_t)
    int inotify_rm_watch(int, uint32_t)


cdef extern from "sys/ioctl.h":
    int ioctl(int fd, unsigned long request, ...)
    unsigned long FIONREAD


cdef extern from "Python.h":
    object PyString_FromStringAndSize(char *, size_t len)
    void *PyMem_Malloc(size_t)
    void PyMem_Free(void *)


def read_from_inotify(int fd):
    cdef char *buf
    cdef unsigned int queue_len
    cdef ssize_t count

    if ioctl(fd, FIONREAD, &queue_len) < 0:
        return ''

    if queue_len <= 0:
        return ''

    buf = <char *>PyMem_Malloc(queue_len)
    if buf == NULL:
        return ''

    count = read(fd, buf, queue_len)
    if count > 0:
        s = PyString_FromStringAndSize(buf, count)
    else:
        s = ''

    PyMem_Free(buf)
    return s


IN_ACCESS = C_IN_ACCESS
IN_MODIFY = C_IN_MODIFY
IN_ATTRIB = C_IN_ATTRIB
IN_CLOSE_WRITE = C_IN_CLOSE_WRITE
IN_CLOSE_NOWRITE = C_IN_CLOSE_NOWRITE
IN_OPEN = C_IN_OPEN
IN_MOVED_FROM = C_IN_MOVED_FROM
IN_MOVED_TO = C_IN_MOVED_TO
IN_CREATE = C_IN_CREATE
IN_DELETE = C_IN_DELETE
IN_DELETE_SELF = C_IN_DELETE_SELF
IN_MOVE_SELF = C_IN_MOVE_SELF
IN_UNMOUNT = C_IN_UNMOUNT
IN_Q_OVERFLOW = C_IN_Q_OVERFLOW
IN_IGNORED = C_IN_IGNORED
IN_CLOSE = C_IN_CLOSE
IN_MOVE = C_IN_MOVE
IN_ONLYDIR = C_IN_ONLYDIR
IN_DONT_FOLLOW = C_IN_DONT_FOLLOW
IN_MASK_ADD = C_IN_MASK_ADD
IN_ISDIR = C_IN_ISDIR
IN_ONESHOT = C_IN_ONESHOT
IN_ALL_EVENTS = C_IN_ALL_EVENTS

def init():
    return inotify_init()

def add_watch(fd, path, mask):
    return inotify_add_watch(fd, path, mask)

def rm_watch(fd, wd):
    return inotify_rm_watch(fd, wd)
