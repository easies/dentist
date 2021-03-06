#!/usr/bin/env python

from . import dentist
from .watchers import LogNotify, Notifier, Poller
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
    parser.add_option('-l', '--log_file', dest='log_file', metavar='PATH',
                      default=None)
    return parser.parse_args()


def main():
    options, args = parse()

    log_kwargs = {
        'level': logging.INFO,
        'format': '%(asctime)-15s %(levelname)-8s %(message)s',
    }

    if options.log_file is not None:
        log_kwargs['filename'] = options.log_file

    logging.basicConfig(**log_kwargs)

    access_logs = options.access_logs
    error_logs = options.error_logs

    if len(access_logs) == 0 and len(error_logs) == 0:
        sys.stderr.write('You must specify at least one log.\n')
        return 1

    # Make the list into a set, so we don't duplicate
    access_logs = set(map(os.path.abspath, access_logs))
    error_logs = set(map(os.path.abspath, error_logs))

    # Set the output directory of the user's logs
    if options.output_dir:
        dentist.LogReader.set_output_directory(options.output_dir)

    poller = Poller()

    # Setup the log readers
    # Add the customized prefixes
    clr = dentist.CombinedLogReader
    clr.add_prefix(*options.prefixes)
    # Set the root of the home directories
    elr = dentist.ErrorLogReader
    elr.configure(homedir_root=options.parent_user_dir)

    notifier = Notifier()

    # Create the list of files and log the set of their directories.
    directories = set()
    for f in access_logs:
        notifier.add_log_notify(LogNotify(f, clr))
    for f in error_logs:
        notifier.add_log_notify(LogNotify(f, elr))

    poller.register(notifier.inotify.fileno(), notifier.handler)

    if options.daemonize:
        from .daemonize import daemonize
        daemonize()

    try:
        while True:
            poller.poll()
    except KeyboardInterrupt:
        logging.shutdown()
        return 0


if __name__ == '__main__':
    sys.exit(main())
