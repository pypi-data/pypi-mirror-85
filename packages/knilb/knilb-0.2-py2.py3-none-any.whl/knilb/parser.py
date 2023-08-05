"""Parser for the knilb package.

"""
import argparse
import os
import uuid
import logging


def parse_args():
    """Parse user command line input to create an :obj:`knilb.Agent`.

    Returns:
        :obj:`argparse.Namespace`: command line arguments.

    """
    parser = argparse.ArgumentParser(prog=__package__,
                                     description='Reference implementation')
    parser.add_argument('cloud', help='Cloud URL')
    parser.add_argument('passkey', help='Cloud API Key')
    parser.add_argument('-u', dest='uuid',
                        default=str(uuid.getnode()),
                        help='Default is local UUID')
    filename = os.path.join(os.path.abspath(__package__),'mock.ini')
    parser.add_argument('-m', dest='mock', type=argparse.FileType(),
                        nargs='?', const=filename, default=os.devnull,
                        help='Config file for mock API.')
    parser.add_argument('-r', '--register', action='store_true',
                        help='Register the Agent then exit.  No testing.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose debug statements.')
    parser.add_argument('-s', '--step', action='store_true',
                        help='Requires you to PRESS ENTER during run time.')

    return parser.parse_args()
