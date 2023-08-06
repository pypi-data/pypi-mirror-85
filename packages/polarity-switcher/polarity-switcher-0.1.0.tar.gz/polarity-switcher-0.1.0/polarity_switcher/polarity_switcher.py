""" Logging module for the Polarity Switcher.
The module manages a :class:`~Daemon.Daemon`
object over TCP communication.
"""

# Imports
from sys import argv
from configparser import Error as ConfigError
from argparse import ArgumentParser, Namespace
from serial import SerialException

# Third party
from zc.lockfile import LockError
from lab_utils.socket_comm import Client
from lab_utils.custom_logging import configure_logging, getLogger
from psycopg2 import DatabaseError

# Local packages
from polarity_switcher.Daemon import Daemon
from polarity_switcher.__project__ import (
    __documentation__ as docs_url,
    __module_name__ as module,
    __description__ as prog_desc,
)


def polarity_switcher():
    """The main routine. It parses the input argument and acts accordingly."""

    # The argument parser
    ap = ArgumentParser(
        prog=module,
        description=prog_desc,
        add_help=True,
        epilog='Check out the package documentation for more information:\n{}'.format(docs_url)
    )

    # Optional arguments
    ap.add_argument(
        '-l',
        '--logging-config-file',
        help='configuration file with the logging options',
        default=None,
        dest='logging_config_file',
        type=str,
    )
    ap.add_argument(
        '-s',
        '--server-config-file',
        help='configuration file with the Alarm Manager options',
        default=None,
        dest='server_config_file',
        type=str,
    )
    ap.add_argument(
        '-d',
        '--device-config-file',
        help='configuration file with the device options',
        default=None,
        dest='device_config_file',
        type=str,
    )
    ap.add_argument(
        '-db',
        '--database-config-file',
        help='configuration file with the Database options',
        default=None,
        dest='database_config_file',
        type=str,
    )
    ap.add_argument(
        '-a',
        '--address',
        help='host address',
        default=None,
        dest='host',
        type=str
    )
    ap.add_argument(
        '-p',
        '--port',
        help='host port',
        default=None,
        dest='port',
        type=int
    )

    # Mutually exclusive positional arguments
    pos_arg = ap.add_mutually_exclusive_group()
    pos_arg.add_argument(
        '--run',
        action='store_true',
        help='starts the Polarity Switcher daemon',
        default=False,
    )
    pos_arg.add_argument(
        '--control',
        type=str,
        help='send a [CONTROL] command to the running Polarity Switcher daemon',
        nargs='?',
    )

    # Auto-start option for supervisord
    ap.add_argument(
        '--autostart',
        action='store_true',
        help='start the daemon, connect to the device and start monitoring',
        default=False,
        dest='autostart',
    )

    # Parse the arguments
    args, extra = ap.parse_known_args(args=argv[1:])
    if extra is not None and args.control is not None:
        args.control += ' ' + ' '.join(extra)

    # Call appropriate function
    if args.run:
        run(args)
    else:
        send_message(args)


def send_message(args: Namespace):
    """ Sends a string message to a running Polarity Switcher
    :class:`Daemon` object over TCP."""

    try:
        # Start a client
        c = Client(
            config_file=args.server_config_file,
            host=args.host,
            port=args.port,
        )
        print('Opening connection to the Polarity Switcher server on {h}:{p}'.format(
            h=c.host,
            p=c.port
        ))

        # Send message and get reply
        print('Sending message: ', args.control)
        reply = c.send_message(args.control)
        print('Reply:\n', reply)

    except ConfigError:
        print('Did you provide a valid configuration file?')

    except OSError:
        print('Maybe the Polarity Switcher server is not running, or running elsewhere')

    except BaseException as e:
        # Undefined exception, full traceback to be printed
        print("{}: {}".format(type(e).__name__, e))

    else:
        exit(0)

    # Something went wrong...
    exit(1)


def run(args: Namespace):
    """ Launches a Polarity Switcher
    :class:`Daemon` object."""

    try:
        # Setup logging
        configure_logging(
            config_file=args.logging_config_file,
            logger_name='Polarity Switcher'
        )

        # Start the daemon, might raise many exceptions
        getLogger().info('Starting the Polarity Switcher server...')
        the_daemon = Daemon(
            config_file=args.server_config_file,
            pid_file_name='/tmp/polaritySwitcher.pid',
            host=args.host,
            port=args.port,
            autostart=args.autostart,
            device_config_file=args.device_config_file,
            database_config_file=args.database_config_file,
        )

        the_daemon.start_daemon()
        getLogger().info('Polarity Switcher server stopped, bye!')

    except DatabaseError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Database initialization error')

    except SerialException as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Device connection error')

    except ConfigError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Did you provide valid configuration files?')

    except OSError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Possible socket error, do you have permissions to the socket?')

    except LockError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Polarity Switcher daemon is probably running elsewhere.')

    except BaseException as e:
        # Undefined exception, full traceback to be printed
        getLogger().exception("{}: {}".format(type(e).__name__, e))

    else:
        exit(0)

    # Something went wrong...
    exit(1)
