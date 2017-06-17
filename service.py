#!/usr/bin/env python
"""SSH Connect in PYTHONIC way

Usage:
    service
    service --jsonfile=<str>
    service -v | --version
    service -h | --help

Options:
    -h, --help      Show this message
    --jsonfile<str> Choose your json connection file
    -v, --version   Show version
"""

__version__ = "0.1"

from core import sshconnect
from docopt import docopt
from sshconnect import settings
from sys import exit


if __name__ == '__main__':
    try:
        arguments = docopt(__doc__, version=__version__)

        if arguments['--jsonfile']:
            connections = sshconnect.get_connections(arguments['--jsonfile'])
        else:
            connections = sshconnect.get_connections('{}/sshconnect.json'.format(settings.BASE_DIR))

        sshconnect.connect_to(sshconnect.select_connection(connections=connections))
    except KeyboardInterrupt:
        exit(1)
