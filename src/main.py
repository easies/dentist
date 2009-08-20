#!/usr/bin/env python

import dentist
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)

    f1 = './access.log'
    clr = dentist.CombinedLogReader()
    fw = dentist.FileWatcher(f1, clr)
    dw = dentist.DirWatcher('.', [fw])

    poller = dentist.Poller()
    poller.register_file_watcher(fw)
    while True:
        poller.poll()


if __name__ == '__main__':
    main()
