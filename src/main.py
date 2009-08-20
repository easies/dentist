#!/usr/bin/env python

import dentist
import logging


def parse():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-n', '--nodaemonize', dest='nodaemonize',
                      action='store_false', default=True)
    parser.add_option('-d', '--directory', dest='directory',
                      metavar='PATH', help='The directory to watch.',
                      default='/tmp/lee')
    parser.add_option('-a', '--access_log', dest='access_logs',
                      action='append', default=[])
    parser.add_option('-e', '--error_log', dest='error_logs',
                      action='append', default=[])
    parser.add_option('-p', '--parent_user_dir', dest='parent_user_dir',
                      default='/home')
    parser.add_option('-o', '--output_dir', dest='output_dir')

    return parser.parse_args()


def main():
    options, args = parse()

    directory = options.directory
    access_logs = options.access_logs
    error_logs = options.error_logs

    if len(access_logs) == 0 and len(access_logs) == 0:
        import sys
        sys.stderr.write('Must specify at least one log.\n')
        return

    logging.basicConfig(level=logging.DEBUG)
    poller = dentist.Poller()
    clr = dentist.CombinedLogReader
    elr = dentist.ErrorLogReader
    elr.configure(homedir_root=options.parent_user_dir)

    fws = []
    for f in access_logs:
        fws.append(dentist.FileWatcher(f, clr, poller))
    for f in error_logs:
        pass
    
    dw = dentist.DirWatcher(directory, fws)
    
    if not options.nodaemonize:
        pass

    while True:
        poller.poll()


if __name__ == '__main__':
    main()
