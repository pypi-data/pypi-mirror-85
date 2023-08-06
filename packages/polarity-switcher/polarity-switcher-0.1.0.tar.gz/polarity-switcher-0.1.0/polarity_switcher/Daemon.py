""" Daemon TCP server. The server will run indefinitely
listening on the specified TCP (see the
:class:`~lab_utils.socket_comm.Server` documentation).
When a client connects and sends a message string, the
message parser will call the appropriate method. The
following commands are supported by the parser (options
must be used with a double dash \\- \\-):

+-----------+-----------------------+---------------------------------------------------------------------------+
| quit      |                       | Stops the daemon and cleans up database and serial port                   |
+-----------+-----------------------+---------------------------------------------------------------------------+
| status    |                       | TODO: Not implemented yet                                                 |
+-----------+-----------------------+---------------------------------------------------------------------------+
| tpg_256a  | on/off/restart        | Connects / disconnects / restarts the TPG 256A device                     |
+           +-----------------------+---------------------------------------------------------------------------+
|           | test                  | Performs a serial port test and returns the device firmware               |
+           +-----------------------+---------------------------------------------------------------------------+
|           | config {file}         | Reloads the default (or given) config file (logging is stopped)           |
+           +-----------------------+---------------------------------------------------------------------------+
|           | gauge-info            | Returns gauge type, status and latest value                               |
+           +-----------------------+---------------------------------------------------------------------------+
|           | single-readout        | Performs a single read-out to the device (logging is stopped)             |
+-----------+-----------------------+---------------------------------------------------------------------------+
| logging   | start / stop          | Launches or stops the separate device monitoring thread                   |
+           +-----------------------+---------------------------------------------------------------------------+
|           | terminal              | Prints output to the terminal with *info* level                           |
+           +-----------------------+---------------------------------------------------------------------------+
|           | use-database          | Enables data saving to a PostgreSQL database                              |
+-----------+-----------------------+---------------------------------------------------------------------------+

"""

# Imports
from serial import SerialException
import argparse
from psycopg2 import DatabaseError
from configparser import Error as ConfigError

# Third party
from lab_utils.socket_comm import Server

# Local
from .PolaritySwitcher import PolaritySwitcher
from .Monitor import Monitor
from .__project__ import (
    __documentation__ as docs_url,
    __description__ as prog_desc,
    __module_name__ as mod_name,
)


class Daemon(Server):
    """ Base class of the daemon, derived from
    :class:`~lab_utils.socket_comm.Server`. The daemon
    holds pointers to the :attr:`device` driver and the
    :attr:`monitor` thread, and communicates with them
    upon message reception. """

    # Attributes
    device: PolaritySwitcher    #: Device handler.
    monitor: Monitor = None     #: Monitor thread.

    use_db: bool
    db_file: str
    use_terminal: bool

    def __init__(self,
                 config_file: str = None,
                 pid_file_name: str = None,
                 host: str = None,
                 port: int = None,
                 autostart: bool = False,
                 device_config_file: str = None,
                 database_config_file: str = None,
                 ):
        """ Initializes the :class:`Daemon` object.
        The :attr:`device` constructor is called and
        serial connection is established.

        Parameters
        ----------
        config_file : str, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        pid_file_name : str, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        host : int, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        port : int, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        autostart : bool, optional
            Connect to the device and start monitoring.

        device_config_file : str, optional
            Configuration file for the Polarity Switcher :attr:`device`.

        database_config_file : str, optional
            Configuration file for the database. If given and
            :paramref:`~Daemon.__init__.autostart` is 'True',
            a :class:`Monitor` thread will be launched with
            database option active.

        Raises
        ------
        :class:`configparser.Error`
            Configuration file error

        :class:`LockError`
            The PID file could not be locked (see parent
            class :class:`~lab_utils.socket_comm.Server`).

        :class:`OSError`
            Socket errors (see parent class
            :class:`~lab_utils.socket_comm.Server`).

        :class:`~serial.SerialException`
            The connection to the :attr:`device` has failed

        :class:`psycopg2.DatabaseError`
            Database initialization error
        """

        # Initialize attributes
        self.use_db = database_config_file is not None
        self.db_file = database_config_file
        self.use_terminal = False

        # Call the parent class initializer, might raise ConfigError, LockError or OSError
        super().__init__(
            config_file=config_file,
            pid_file_name=pid_file_name,
            host=host,
            port=port,
        )

        # Add custom arguments to the message parser
        self.update_parser()

        # Initialize device, might raise ConfigError or SerialException
        self.device = PolaritySwitcher(config_file=device_config_file)

        # Autostart?
        if not autostart:
            return
        else:
            self.logger.info('Launching auto-start sequence')

        # Start background monitor thread, might raise ConfigError or DatabaseError
        self.monitor = Monitor(
            device=self.device,
            name='Daemon Thread',
            terminal_flag=False,    # the autostart option is meant to be used with supervisord, no terminal output
            database_flag=database_config_file is not None,
            database_config_file=database_config_file,
        )
        self.logger.info('Monitor thread launched!')

    def update_parser(self):
        """ Sets up the message
        :attr:`~lab_utils.socket_comm.Server.parser`. """

        self.logger.debug('Setting up custom message parser')

        # Set some properties of the base class argument parser
        self.parser.prog = mod_name
        self.parser.description = prog_desc
        self.parser.epilog = 'Check out the package documentation for more information:\n{}'.format(docs_url)

        # Subparsers for each acceptable command
        # 1. STATUS
        sp_status = self.sp.add_parser(
            name='status',
            description='checks the status of the daemon',
        )
        sp_status.set_defaults(
            func=self.status,
            which='status')

        # 2. DEVICE
        sp_control = self.sp.add_parser(
            name='control',
            description='interface to the Polarity Switcher device',
        )
        sp_control.set_defaults(
            func=self.control,
            which='control'
        )
        sp_g1 = sp_control.add_mutually_exclusive_group()
        sp_g1.add_argument(
            '--on',
            action='store_true',
            help='connects to the device',
            default=False,
            dest='turn_on',
        )
        sp_g1.add_argument(
            '--off',
            action='store_true',
            help='closes the connection',
            default=False,
            dest='turn_off',
        )
        sp_g1.add_argument(
            '--restart, -r',
            action='store_true',
            help='restarts the connection',
            default=False,
            dest='restart',
        )
        sp_control.add_argument(
            '--config,-c',
            default=argparse.SUPPRESS,      # If --config is not given,  it will not show up in the namespace
            nargs='?',                      # If --config is given, it may be used with or without an extra argument
            const=None,                     # If --config is given without an extra argument, 'dest' = None
            help='reloads the configuration file (and resets the file if given, absolute path only)',
            dest='config_file',
        )

        # 3. MONITOR
        sp_monitor = self.sp.add_parser(
            name='logging',
            description='manages the logging thread',
        )
        sp_monitor.set_defaults(
            func=self.logging,
            which='logging'
        )
        sp_g2 = sp_monitor.add_mutually_exclusive_group()
        sp_g2.add_argument(
            '--start',
            action='store_true',
            help='starts the monitor thread',
            default=False,
            dest='start',
        )
        sp_g2.add_argument(
            '--stop',
            action='store_true',
            help='stops the monitor thread',
            default=False,
            dest='stop',
        )
        sp_monitor.add_argument(
            '--terminal',
            action='store_true',
            help='prints the monitor output to the application logging sink',
            default=False,
            dest='terminal',
        )
        sp_monitor.add_argument(
            '--use-database',
            default=argparse.SUPPRESS,  # If --use-database is not given it will not show up in the namespace
            nargs='?',                  # If --use-database is given it may be used with or without an extra argument
            const=None,                 # If --use-database is given without an extra argument, 'dest' = None
            help='logs data to a PostgreSQL database using the given config file, or the default one',
            dest='database_config_file',
        )

        # 4. AO - Analog Outputs
        sp_ao = self.sp.add_parser(
            name='ao',
            description='analog outputs control',
        )
        sp_ao.set_defaults(
            func=self.an_out,
            which='dac'
        )
        sp_ao.add_argument(
            '--id',
            dest='id',
            type=int,
            choices=range(3),
            help='output ID: 0, 1 or 2',
            required=True
        )
        sp_ao.add_argument(
            '--value',
            dest='value',
            type=float,
            help='output level, in Volt',
            required=True
        )

        # 5. DO - Digital Outputs
        sp_dig_out = self.sp.add_parser(
            name='do',
            description='digital outputs control',
        )
        sp_dig_out.set_defaults(
            func=self.dig_out,
            which='do'
        )
        sp_dig_out.add_argument(
            '--id',
            dest='id',
            type=int,
            choices=range(5),
            help='output ID: 0 to 4',
            required=True
        )
        sp_dig_out_level = sp_dig_out.add_mutually_exclusive_group(required=True)
        sp_dig_out_level.add_argument(
            '--on',
            action='store_true',
            help='sets the output to ON (1)',
            dest='value',
        )
        sp_dig_out_level.add_argument(
            '--off',
            action='store_false',
            help='sets the output to OFF (0)',
            dest='value',
        )

    def quit(self):
        """ Stops the daemon, called with message 'quit'.
        The method overrides the original
        :meth:`~lab_utils.socket_comm.Server.quit` to do
        proper clean-up of the monitoring
        :attr:`thread<monitor>` and the :attr:`device`
        handler.
        """

        self.logger.info('Launching quitting sequence')

        # Monitor
        if self.monitor is not None and self.monitor.is_alive():
            if self.monitor.stop():
                self.reply += 'Monitor thread stopped\n'
            else:
                self.reply += 'Thread error! Monitor thread did not respond to the quit signal and is still running\n'

        # Serial connection
        self.device.disconnect()
        self.reply += 'Clean-up: device is now off\n'
        self.logger.info('Serial connection closed')

        self.logger.info('Stopping daemon TCP server now')
        self.reply += 'Stopping daemon TCP server now'

    def status(self):
        """ TODO
        """
        self.reply += 'Status: doing great!'

    def control(self):
        """ Modifies or checks the status of the Polarity Switcher
        :attr:`device`. Provides functionality to:

        -  Connect and disconnect the controller.
        -  Reload device configuration.
        """
        self.logger.debug('Method \'control\' called by the message parser')

        # Restart device
        if self.namespace.restart:
            try:
                self._restart_device()
            except BaseException as e:
                self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                return
            self.reply += 'Device was restarted\n'

        # Reset and load configuration file
        if "config_file" in self.namespace:
            try:
                self._reload_config()
            except BaseException as e:
                self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                return

            self.reply += 'Device was reconfigured\n'
            if self.namespace.config_file is not None:
                self.reply += 'New configuration file: {}\n'.format(self.device.config_file)

        self.reply += 'Control routine completed\n'

    def _reload_config(self):
        """ Reloads the device configuration. If the device
        was initially logging, it is also stopped and
        relaunched afterwards.

        Raises
        ------
        :class:`configparser.Error`
            Database configuration file error.

        :class:`psycopg2.DatabaseError`
            Database error (connection, access...)

        :class:'RuntimeError`
            The monitor thread could not be stopped within 5 seconds, or the device was busy for too long.

        :class:`~serial.SerialException`
            The connection to the device has failed

        :class:`ValueError`
           Invalid default parameters in the freshly loaded configuration file.
        """

        self.logger.info('Reloading device configuration')

        # Stop logging, reconnect, and start logging if necessary
        logging_active = self._is_logging()
        if logging_active:
            self.logger.debug('Saving logging configuration to relaunch')
            # Save current configuration of the logging thread
            self.namespace.terminal = self.monitor.terminal_flag
            if self.monitor.database_flag:
                self.namespace.database_config_file = self.monitor.database_config_file

            # Stop the thread, might raise RuntimeError
            self._stop_logging(quiet=True)

        # Reconfigure device, might raise ConfigError
        self.device.config(new_config_file=self.namespace.config_file)

        # Apply device output defaults, might raise ValueError, SerialException or RuntimeError
        self.device.apply_defaults()

        # Start logging if necessary, might raise
        if logging_active:
            self._start_logging()

    def _restart_device(self):
        """ Restarts the device. If the device was initially
        logging, it is also stopped and relaunched afterwards.

        Raises
        ------
        :class:'lakeshore.InstrumentException`
            Lakeshore 336 device error

        :class:`configparser.Error`
            Database configuration file error.

        :class:`psycopg2.DatabaseError`
            Database error (connection, access...)

        :class:'RuntimeError`
            The monitor thread could not be stopped within 5 seconds.
        """

        self.logger.info('Initializing restart sequence')

        # Stop logging, reconnect, and start logging if necessary
        logging_active = self._is_logging()
        if logging_active:
            self._stop_logging(quiet=True)

        self.device.reconnect()

        if logging_active:
            self._start_logging()

    def logging(self):
        """ Manages the :attr:`logging thread<monitor>`.
        Provides functionality to start and stop the thread.
        """
        self.logger.debug('Method \'logging\' called by the message parser')

        # Use database
        self.use_db = "database_config_file" in self.namespace
        if self.use_db:
            self.db_file = self.namespace.database_config_file

        # Use terminal
        self.use_terminal = self.namespace.terminal

        # Start
        if self.namespace.start:
            try:
                self._start_logging()
                self.reply += 'Daemon Thread launched\nYou can check its status with the \'status\' option\n'
            except (SerialException, RuntimeError, DatabaseError, ConfigError) as e:
                self.reply += 'Error launching Daemon Thread! {}: {}'.format(type(e).__name__, e)
                return

        # Stop
        if self.namespace.stop:
            try:
                self._stop_logging()
                self.use_db = False
                self.db_file = ''
                self.use_terminal = False
                self.reply += 'Daemon thread stopped\n'
            except RuntimeError as e:
                self.reply += 'Error stopping Daemon Thread! {}: {}'.format(type(e).__name__, e)
                return

    def _is_logging(self) -> bool:
        """ Checks whether the :attr:`logging thread<monitor>` is running.

        Returns
        -------
        bool
            True if the monitor is running, False otherwise.

        """
        return self.monitor is not None and self.monitor.is_alive()

    def _start_logging(self):
        """ Creates and starts the :attr:`logging thread<monitor>`.

        Raises
        ------
        :class:`configparser.Error`
            Database configuration file error.

        :class:`psycopg2.DatabaseError`
            Database error (connection, access...)

        """
        # Check the monitor is not running yet
        if self._is_logging():
            self.logger.warning('Monitor thread is already running')
            self.reply += 'Monitor thread is already running\n'
            return

        # Launch monitor thread, might raise ConfigError or DatabaseError
        self.logger.info('Launching logging thread')
        self.monitor = Monitor(
            device=self.device,
            name='Daemon Thread',
            terminal_flag=self.use_terminal,
            database_flag=self.use_db,
            database_config_file=self.db_file,
        )

    def _stop_logging(self, quiet: bool = False):
        """ Signals a running :attr:`logging thread<monitor>` to stop.

        Parameters
        ----------
        quiet : bool, optional
            If True, no output is produced for the initial running check

        Raises
        -------
        :class:'RuntimeError`
            The monitor thread could not be stopped within 5 seconds.
        """

        # Check monitor is actually running
        if not self._is_logging():
            if not quiet:
                self.logger.info('Monitor thread is not running')
                self.reply += 'Monitor thread is not running\n'
            return

        # Signal the monitor to stop, might raise RuntimeError
        self.logger.info('Stopping logging thread')
        self.monitor.stop()

    def an_out(self):
        """ Sets the analog output of the Polarity Switcher
        :attr:`device`.
        """
        self.logger.debug('Method \'an_out\' called by the message parser')

        # Set the analog output
        try:
            self.device.set_analog_output(self.namespace.id, self.namespace.value)
        except BaseException as e:
            self.reply += 'Error setting analog output! {}: {}'.format(type(e).__name__, e)
            return
        self.reply += 'Analog output {} set to {}V'.format(self.namespace.id, self.namespace.value)

    def dig_out(self):
        """ Sets the digital output of the Polarity Switcher
        :attr:`device`.
        """
        self.logger.debug('Method \'dig_out\' called by the message parser')

        # Set the analog output
        try:
            self.device.set_digital_output(self.namespace.id, self.namespace.value)
        except BaseException as e:
            self.reply += 'Error setting digital output! {}: {}'.format(type(e).__name__, e)
            return
        self.reply += 'Digital output {} set to {}'.format(self.namespace.id, int(self.namespace.value))
