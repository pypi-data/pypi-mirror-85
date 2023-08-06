""" Background monitoring thread based on the :obj:`threading`
library. A :obj:`Monitor` object starts a background
:class:`thread<threading.Thread>` which reads out the Polarity Switcher
:attr:`~Monitor.device` every second. The data can then be
printed to the terminal and/or saved to a PostgreSQL database
using the :obj:`lab_utils.database` library. The monitoring
thread is intended to be self-sustainable and will try to deal
with unexpected errors (usually issues with communication to
the device), recover, log them and keep running.
"""

# Imports
from time import sleep, time
from threading import Thread, Event
from typing import List
from itertools import chain

# Third party
from lab_utils.database import Database
from lab_utils.custom_logging import getLogger
from serial.serialutil import SerialException
from psycopg2 import Error as DatabaseError, Warning as DatabaseWarning

# Local
from .PolaritySwitcher import PolaritySwitcher


class Monitor(Thread):
    """ Manages a background
    :class:`thread<threading.Thread>`
    which logs data from the Polarity Switcher
    :attr:`~Monitor.device`."""

    # Thread objects
    device: PolaritySwitcher    #: :class:`Polarity Switcher device<.PolaritySwitcher>` handler.
    db: Database                #: :class:`Database<lab_utils.database.Database>` object.

    # Thread flags
    run_flag: Event         #: :class:`Flag<threading.Event>` to signal the thread to stop.
    database_flag: Event    #: Database usage :class:`flag<threading.Event>`.
    terminal_flag: Event    #: Terminal output :class:`flag<threading.Event>`.

    # Monitor Variables
    refresh_rate: int           #: Logging refresh rate
    database_config_file: str   #: Database configuration file
    table_name: str             #: Name of the PostgreSQL table where data will be saved.
    column_list: List[str]      #: :class:`~typing.List` of data labels to save.

    def __init__(self,
                 device: PolaritySwitcher,
                 name: str = 'Monitor Thread',
                 database_flag: bool = False,
                 database_config_file: str = None,
                 terminal_flag: bool = False,
                 table_name: str = 'polarity_switcher'):
        """ Initializes the :class:`Monitor` object. The
        constructor checks that the given :paramref:`device`
        is initialized. If :paramref:`database_flag` is set
        to `True`, the :meth:`prepare_database` method is
        called, which initializes the :attr:`database<db>`
        object and sets up the connection. A table named
        :paramref:`table_name` is created, as well as the
        necessary :attr:`columns<column_list>` to store the
        temperature data.

        Finally, the method :meth:`run` starts and detaches
        a background thread which will run indefinitely,
        reading the Polarity Switcher :attr:`device`. The data is
        saved to the :attr:`database` if :paramref:`database_flag`
        is set to `True`, and it is printed to the terminal if
        :paramref:`terminal_flag` is set to `True`.

        Parameters
        ----------
        device: :class:`.PolaritySwitcher`
            Device handle, must be already initialized and connected.

        name: str, optional
            Thread name for logging purposes, default is 'Monitor Thread'

        database_flag: bool, optional
            Save data to a PostgreSQL database, default is 'False'

        terminal_flag: bool, optional
            Print data to the logging terminal sink with 'info'
            level, default is 'False'

        table_name: str, optional
            Name of the PostgreSQL table where the data is saved, default is 'polarity_switcher'.


        Raises
        ------

        :class:`configparser.Error`
            Database configuration file error.

        :class:`psycopg2.DatabaseError`
            Database error (connection, access...)
        """

        # Assign arguments
        self.table_name = table_name

        # Check device is ON and ready
        self.device = device

        # Retrieve refresh rate from device
        self.refresh_rate = self.device.refresh_rate

        # Call the parent class initializer
        super().__init__(name=name)

        # Initialize flags
        self.run_flag = Event()
        self.database_flag = Event()
        self.terminal_flag = Event()

        # Database flag must come with a database configuration file
        if database_flag and database_config_file is None:
            getLogger().warning('Database flag set to True, but no configuration file provided')
            database_flag = False

        # Set flags
        self.run_flag.set()
        if database_flag:
            getLogger().info('Database option active')
            self.database_flag.set()
        else:
            getLogger().info('Database option not active')

        if terminal_flag:
            getLogger().info('Terminal option active')
            self.terminal_flag.set()
        else:
            getLogger().info('Terminal option not active')

        # Initialize database, might raise ConfigError or DatabaseError
        self.database_config_file = database_config_file
        if database_flag:
            self.prepare_database()

        # Run
        self.start()

    def prepare_database(self):
        """ Ensures the :attr:`database<db>` is ready to accept
        data from the Polarity Switcher :attr:`device`. Initializes
        the :attr:`database<db>` object and sets up the
        connection. If the table :attr:`table_name` does not
        exist, it is created, as well as the necessary
        :attr:`columns<column_list>` to store the device
        data.

        Raises
        ------
        :class:`configparser.Error`
            Error reading configuration file.

        :class:`psycopg2.Error`
            Base exception for all kinds of database errors.

        """

        getLogger().info('Setting up database')
        self.db = Database(config_file=self.database_config_file)   # might raise ConfigError
        self.db.connect(print_version=True)                         # might raise DatabaseError

        # Check table exists, create otherwise
        if not self.db.check_table(self.table_name):
            self.db.create_timescale_db(self.table_name)
            if not self.db.check_table(self.table_name):
                raise RuntimeError('could not create TimescaleDB object \'%s\'', self.table_name)
        getLogger().debug('Table \'%s\' ready', self.table_name)

        # Create column list looping over device features
        self.column_list = []

        for f in chain(
            self.device.analog_inputs,
            self.device.analog_outputs,
            self.device.digital_outputs,
            self.device.switches
        ):
            if f.active:
                self.column_list.append(f.db_label)
                self.db.new_column(
                    table_name=self.table_name,
                    column_name=f.db_label,
                    data_type=f.db_type,
                    constraints=None,
                )
                getLogger().debug('Column \'%s\' ready', f.db_label)

        # Recreate aggregate view
        self.db.create_aggregate_view(table_name=self.table_name)

    def stop(self) -> bool:
        """ Clears the :attr:`run_flag` to signal the
        background thread to stop. The thread status is
        then checked every 0.1 second (up to 5 seconds).

        Raises
        -------
        :class:'RuntimeError`
            The monitor thread could not be stopped within 5 seconds.
        """

        getLogger().info('Sending stop signal to the logging thread')
        self.run_flag.clear()

        # Check thread status every 0.1 seconds, for 5 seconds
        for _ in range(50):
            if not self.is_alive():
                getLogger().info('Monitor thread successfully stopped')
                return True
            sleep(0.1)

        # Thread should have stopped by now, something went wrong
        getLogger().error('Monitor thread did not finish within a reasonable time')
        raise RuntimeError('Monitor thread did not finish within a reasonable time.')

    def run(self) -> None:
        """ Monitoring method start upon object creation.
        The Polarity Switch :attr:`device` is read every second
        in an endless loop. The device status may be saved
        to a PostgreSQL :attr:`database<db>` and/or printed
        to the terminal, if the respective :attr:`terminal_flag`
        and :attr:`database_flag` flags were set.

        In case of unexpected error (which happens often with
        the RS-232 communication protocol), the method will
        try to recover, log any information and continue operations.

        To stop logging and break the loop, the :meth:`stop`
        method should be used to set the :attr:`run_flag` flag.
        """

        # Let the server reply to the client to produce a cleaner log
        sleep(0.1)
        getLogger().info('Starting monitor')

        # Initialize timer
        seconds = int(time())

        # Endless loop, use the stop() method to break it
        while self.run_flag.is_set():
            try:
                # Read temperature data from the device
                self.device.read_inputs()

                # Save to database, might raise DatabaseError or DatabaseWarning
                self.save_to_database()

                # Print to terminal and/or file
                self.print_string()

            except (SerialException, IOError, DatabaseError, DatabaseWarning) as e:
                getLogger().error("{}: {}".format(type(e).__name__, e))
                for i in range(5):
                    sleep(2)
                    getLogger().error('Attempting to reset the device (%d out of 5)', i)
                    try:
                        self.device.reconnect()
                    except SerialException as e2:
                        getLogger().error("{}: {}".format(type(e).__name__, e2))
                    else:
                        # Leave the reconnection "for" loop and return to the main "while" loop
                        break
                # The reconnection attempts have failed, terminate the thread and notify the alarm manager
                getLogger().error('Terminating Polarity Switcher Monitor!')
                raise SystemExit(
                    'Could not re-establish connection to the device after 5 attempts, terminating thread now...'
                )

            # Repeat every refresh_rate seconds
            while int(time()) < seconds + self.refresh_rate and self.run_flag.is_set():
                sleep(0.1)
            seconds = int(time())

        # We reach here when 'run_flag' has been cleared by the stop() method
        getLogger().info('Stop signal! Quitting logging thread')

    def print_string(self):
        """ Prints the retrieved data to the terminal. The log
        level will be `INFO` if :attr:`terminal_flag` is set,
        and `DEBUG` otherwise."""

        # Build message string
        msg = ''

        # Feature: analog inputs
        msg += '{:20}'.format('Analog Inputs:')
        for f in self.device.analog_inputs:
            if f.active:
                msg += '{:20}'.format('{:7}: {}V'.format(f.label, f.value))

        # Print to terminal
        if self.terminal_flag.is_set():
            getLogger().info(msg)
        else:
            getLogger().debug(msg)

    def save_to_database(self):
        """ Saves the latest device data to the
        PostgreSQL :attr:`database<db>`. If
        :attr:`database_flag` is not set, the
        method does nothing.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kinds of database errors.

        :class:`psycopg2.Warning`
            Base exception for all kinds of database warnings.
        """

        if not self.database_flag.is_set() or self.db is None:
            return

        # Prepare data list
        data = []

        # Features: analog inputs, analog outputs
        for f in chain(
            self.device.analog_inputs,
            self.device.analog_outputs,
            self.device.digital_outputs,
            self.device.switches
        ):
            if f.active:
                data.append(f.value)

        # Commit data to the database, might raise DatabaseError or DatabaseWarning
        self.db.new_entry(
            table_name=self.table_name,
            columns=self.column_list,
            data=data,
            check_columns=False,
        )
