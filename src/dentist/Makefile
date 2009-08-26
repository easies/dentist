
CC = gcc
CFLAGS = -g -Wall
all: _inotify.so

_inotify.c:
	pyrexc _inotify.pyx

_inotify.o: _inotify.c
	$(CC) $(CFLAGS) -c -o _inotify.o -I /proj/crew/lee/usr/include/python2.6 -I /proj/crew/lee/usr/include _inotify.c

_inotify.so: _inotify.o
	$(CC) $(CFLAGS) -shared -o _inotify.so _inotify.o

clean:
	$(RM) *.o *.so _inotify.c *.pyc
