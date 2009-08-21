#!/usr/bin/env python

import dentist
import logging
import os
import sys


def parse():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-d', '--daemonize', dest='daemonize',
                      action='store_true', default=False)
    parser.add_option('-a', '--access_log', dest='access_logs',
                      action='append', default=[])
    parser.add_option('-p', '--home-prefix', dest='prefixes',
                      action='append', default=[])
    parser.add_option('-e', '--error_log', dest='error_logs',
                      action='append', default=[])
    parser.add_option('-u', '--parent_user_dir', dest='parent_user_dir',
                      default='/home')
    parser.add_option('-o', '--output_dir', dest='output_dir',
                      default=None)
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.DEBUG)

    options, args = parse()

    access_logs = options.access_logs
    error_logs = options.error_logs

    if len(access_logs) == 0 and len(error_logs) == 0:
        sys.stderr.write('You must specify at least one log.\n')
        return 1

    # Make the list into a set, so we don't duplicate
    access_logs = map(os.path.abspath, access_logs)
    access_logs = set(access_logs)
    error_logs = map(os.path.abspath, error_logs)
    error_logs = set(error_logs)

    if not options.output_dir:
        dentist.LogReader.set_output_directory(options.output_dir)

    poller = dentist.Poller()
    clr = dentist.CombinedLogReader
    clr.add_prefix(*options.prefixes)
    elr = dentist.ErrorLogReader
    elr.configure(homedir_root=options.parent_user_dir)

    fws = []
    directories = set()
    for f in access_logs:
        directories.add(os.path.dirname(f))
        fws.append(dentist.FileWatcher(f, clr, poller))
    for f in error_logs:
        directories.add(os.path.dirname(f))
        fws.append(dentist.FileWatcher(f, elr, poller))

    dw = dentist.DirWatcher(directories, fws)
    
    if options.daemonize:
        from daemonize import daemonize
        daemonize()

    try:
        while True:
            poller.poll()
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
