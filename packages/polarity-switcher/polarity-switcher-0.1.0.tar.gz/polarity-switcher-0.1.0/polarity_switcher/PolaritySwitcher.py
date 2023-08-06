""" Driver for the Polarity Switcher. The device is
a...

The :class:`PolaritySwitcher` main class manages the interface
to the device and provides connection and communication
methods through USB.
"""

# Imports
from serial import (
    Serial,
    EIGHTBITS,
    SerialException
)
from typing import List
import configparser
from configparser import Error as ConfigError
from threading import Event
from time import sleep

# Third party
from lab_utils.custom_logging import getLogger
from lab_utils.database import DataType


class Feature:
    """ Global wrapper for every feature of the device"""

    active: bool        #: Logging flag
    label: str          #: Label of the output
    db_prefix: str      #: Database column prefix
    db_label: str       #: Database column label
    db_type: DataType   #: Database variable type
    serial_string: str  #: String to be sent to the device to access the feature

    def __init__(
            self,
            active: bool,
            label: str,
            db_prefix: str,
            db_type: DataType,
    ):
        self.active = active
        self.db_prefix = db_prefix.lower()
        self.db_type = db_type
        self.set_label(label)

    def set_label(self, label: str):
        """ Sets the feature label and database label. """
        self.label = label
        self.db_label = '{}_{}'.format(self.db_prefix, label.lower())


class AnalogInput(Feature):
    """ Analog input wrapper"""

    id: int         #: Channel ID
    value: float    #: Latest value

    def __init__(
            self,
            channel_number: int,
            active: bool,
            label: str,
    ):
        super().__init__(
            active=active,
            label=label,
            db_prefix='ai',
            db_type=DataType.float
        )
        self.id = channel_number
        self.value = float("NaN")
        self.serial_string = 'ADC:{}'.format(self.id)

    def get_serial_string(self) -> str:
        return self.serial_string


class AnalogOutput(Feature):
    """ Analog output wrapper"""

    id: int         #: Channel ID
    value: float    #: Latest value

    def __init__(
            self,
            channel_number: int,
            active: bool,
            label: str,
    ):
        super().__init__(
            active=active,
            label=label,
            db_prefix='ao',
            db_type=DataType.float
        )
        self.id = channel_number
        self.value = float("NaN")
        self.serial_string = 'DAC:{}:'.format(self.id)

    def get_serial_string(self, value: float) -> str:
        return '{}{}'.format(self.serial_string, value)


class DigitalOutput(Feature):
    """ Digital output wrapper"""

    id: int         #: Channel ID
    value: bool     #: Latest value

    def __init__(
            self,
            channel_number: int,
            active: bool,
            label: str,
    ):
        super().__init__(
            active=active,
            label=label,
            db_prefix='do',
            db_type=DataType.bool
        )
        self.id = channel_number
        self.value = False
        self.serial_string = 'DO:{}:'.format(self.id)

    def get_serial_string(self, value: bool) -> str:
        return '{}{}'.format(self.serial_string, int(value))


class Switch(Feature):
    """ Switch wrapper"""

    id: int         #: Switch ID
    value: bool     #: Latest value

    def __init__(
            self,
            channel_number: int,
            active: bool,
            label: str,
    ):
        super().__init__(
            active=active,
            label=label,
            db_prefix='ps',
            db_type=DataType.bool
        )
        self.id = channel_number
        self.value = False
        self.serial_string = 'PS:{}:'.format(self.id)

    def get_serial_string(self, value: bool) -> str:
        return '{}{}'.format(self.serial_string, int(value))


class PolaritySwitcher(object): # noqa (ignore CamelCase convention)
    """ Driver implementation for the Polarity Switcher.
    """

    # Serial port configuration
    serial: Serial      #: Serial port handler.
    baud_rate: int      #: Baud rate for serial communication.
    serial_port: str    #: Physical address of the device file.
    timeout: float      #: Time-out for serial connection error.
    busy: Event         #: Flag to avoid concurrent access to the device

    # Device setup
    config_file: str                        #: Device configuration file
    refresh_rate: int                       #: Logging refresh rate
    analog_inputs: List[AnalogInput]        #: Wrappers for the analog inputs
    analog_outputs: List[AnalogOutput]      #: Wrappers for the analog outputs
    digital_outputs: List[DigitalOutput]    #: Wrappers for the digital outputs
    switches: List[Switch]                  #: Wrappers for the switches

    def __init__(self,
                 config_file: str = 'conf/polaritySwitcher.ini'
                 ):
        """ Initializes the :class:`PolaritySwitcher` object. It calls
        the :meth:`config` method to set up the device with the
        :paramref:`~PolaritySwitcher.__init__.config_file` parameter.

        Parameters
        ----------
        config_file : str, optional
            Configuration file, default is 'conf/polaritySwitcher.ini'.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error

        :class:`~serial.SerialException`
            The connection to the device has failed

        :class:`ValueError`
           Invalid default parameters.

        :class:`RuntimeError`
           Device busy for too long.
        """
        # Initialize variables
        self.busy = Event()
        self.busy.clear()

        self.analog_inputs = []
        for i in range(2):
            self.analog_inputs.append(AnalogInput(i, False, ''))

        self.analog_outputs = []
        for i in range(3):
            self.analog_outputs.append(AnalogOutput(i, False, ''))

        self.digital_outputs = []
        for i in range(5):
            self.digital_outputs.append(DigitalOutput(i, False, ''))

        self.switches = []
        for i in range(5):
            self.switches.append(Switch(i, False, ''))

        # Load config file, might raise ConfigError
        self.config_file = config_file
        self.config(config_file)

        # Connect to the device, might raise SerialException
        self.connect()

        # Apply default outputs, might raise ValueError, SerialException or RuntimeError
        self.apply_defaults()

    def config(self, new_config_file: str = None):
        """ Loads the Polarity Switcher configuration from a file.
        If :paramref:`~PolaritySwitcher.config.new_config_file`
        is not given, the latest :attr:`config_file` is re-loaded;
        if it is given and the file is successfully parsed,
        :attr:`config_file` is updated to the new value.

        Parameters
        ----------
        new_config_file : str, optional
            New configuration file to be loaded.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error
        """

        # Save previous configuration
        old_analog_inputs = self.analog_inputs
        old_analog_outputs = self.analog_outputs

        # Configuration file, if given
        if new_config_file is None:
            new_config_file = self.config_file

        # Try to execute, otherwise revert to previous state
        try:
            # Initialize config parser and read file
            getLogger().info("Loading configuration file %s", new_config_file)
            config_parser = configparser.ConfigParser()
            config_parser.read(new_config_file)

            # Load serial port configuration
            self.serial_port = config_parser.get(section='Connection', option='device')
            self.baud_rate = config_parser.getint(section='Connection', option='baud_rate')
            self.timeout = config_parser.getfloat(section='Connection', option='timeout')
            self.refresh_rate = config_parser.getint(section='Connection', option='refresh_rate')

            # Check sanity
            if self.refresh_rate < 1:
                raise ConfigError('Invalid logging refresh rate: {}'.format(self.refresh_rate))

            # Load analog inputs
            list_labels = []
            for f in self.analog_inputs:
                sec_name = 'AnalogInput_{}'.format(f.id)
                if config_parser.has_section(sec_name):
                    f.active = config_parser.getboolean(sec_name, 'active')
                    f.set_label(config_parser.get(sec_name, 'label'))
                    if f.label in list_labels:
                        raise ConfigError('Duplicate label {}'.format(f.label))
                    else:
                        list_labels.append(f.label)
                    getLogger().debug('Analog input %d: %s, %s', f.id, str(f.active), f.label)
                else:
                    f.active = False
                    f.label = ''

            # Load analog outputs
            list_labels = []
            for f in self.analog_outputs:
                sec_name = 'AnalogOutput_{}'.format(f.id)
                if config_parser.has_section(sec_name):
                    f.active = config_parser.getboolean(sec_name, 'active')
                    f.set_label(config_parser.get(sec_name, 'label'))
                    f.value = config_parser.get(sec_name, 'default')
                    if f.label in list_labels:
                        raise ConfigError('Duplicate label {}'.format(f.label))
                    else:
                        list_labels.append(f.label)
                    getLogger().debug('Analog output %d: %s, %s, %s', f.id, str(f.active), f.label, f.value)
                else:
                    f.active = False
                    f.label = ''
                    f.value = 0.

            # Load digital outputs
            list_labels = []
            for f in self.digital_outputs:
                sec_name = 'DigitalOutput_{}'.format(f.id)
                if config_parser.has_section(sec_name):
                    f.active = config_parser.getboolean(sec_name, 'active')
                    f.set_label(config_parser.get(sec_name, 'label'))
                    f.value = config_parser.getboolean(sec_name, 'default')
                    if f.label in list_labels:
                        raise ConfigError('Duplicate label {}'.format(f.label))
                    else:
                        list_labels.append(f.label)
                    getLogger().debug('Digital output %d: %s, %s, %s', f.id, str(f.active), f.label, f.value)
                else:
                    f.active = False
                    f.label = ''
                    f.value = False

            # Load switches
            list_labels = []
            for f in self.switches:
                sec_name = 'PolaritySwitch_{}'.format(f.id)
                if config_parser.has_section(sec_name):
                    f.active = config_parser.getboolean(sec_name, 'active')
                    f.set_label(config_parser.get(sec_name, 'label'))
                    f.value = config_parser.getboolean(sec_name, 'default')
                    if f.label in list_labels:
                        raise ConfigError('Duplicate label {}'.format(f.label))
                    else:
                        list_labels.append(f.label)
                    getLogger().debug('Switch  %d: %s, %s, %s', f.id, str(f.active), f.label, f.value)
                else:
                    f.active = False
                    f.label = ''
                    f.value = False

            # If everything worked, update local config_file for future calls
            self.config_file = new_config_file

        except Exception as e:
            # Restore previous configuration
            self.analog_inputs = old_analog_inputs
            self.analog_outputs = old_analog_outputs
            raise e

    def connect(self):
        """ Connects to the Polarity Switcher device.

        Raises
        ------
        :class:`~serial.SerialException`
            The connection to the device has failed.
        """
        getLogger().debug('Connecting to Polarity Switcher on port %s', self.serial_port)

        # Open serial connection, might raise SerialException
        self.serial = Serial(
            port=self.serial_port,
            baudrate=self.baud_rate,
            bytesize=EIGHTBITS,
            timeout=self.timeout,
        )

        getLogger().info('Connection to Polarity Switcher on port %s successful', self.serial_port)
        self.flush()

    def disconnect(self):
        """ Closes the connection to the Polarity Switcher.
        """

        getLogger().debug('Closing connection to Polarity Switcher')
        self.serial.close()
        getLogger().info('Connection to Polarity Switcher closed')

    def reconnect(self):
        """ Closes the Polarity Switcher device and connects again.

        Raises
        ------
        :class:`~serial.SerialException`
            The connection to the device has failed.
        """
        getLogger().debug('Reconnecting to Polarity Switcher on port %s', self.serial_port)

        # Close connection
        self.serial.close()

        # Connect again, might raise SerialException
        self.serial = Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                bytesize=EIGHTBITS,
                timeout=self.timeout,
        )
        getLogger().debug('Polarity Switcher reconnected on port on port %s', self.serial_port)

    def command(self, msg: str) -> str:
        """ Send the command string
        :paramref:`~PolaritySwitcher.command.msg` through
        the serial connection. If the port is busy, the
        method waits up to 5 seconds to send the command.

        Parameters
        ----------
        msg : str
            Command to be sent to the device.

        Raises
        ------
        :class:`serial.SerialException`
           Serial communication error

        :class:`RuntimeError`
           Device was busy for too long
        """
        # Avoid concurrent access with the busy flag
        # Try to set the flag for 5 seconds, raise RuntimeError otherwise
        for _ in range(50):
            if not self.busy.is_set():
                self.busy.set()
                getLogger().debug('Device is now locked, ready to receive message \'{}\''.format(msg))
                break
            sleep(0.1)
            getLogger().debug('Device busy, waiting to send message \'{}\'...'.format(msg))
        else:
            raise RuntimeError('Device busy for too long, message \'{}\' not sent'.format(msg))

        # Send the message, might raise SerialException
        getLogger().debug('Sending message \'{}\''.format(msg))
        self.serial.write(msg.encode('utf-8'))

        # Read reply, might raise SerialException
        r = self.serial.readline().decode("utf-8").replace('\n', ' ').replace('\r', '')
        getLogger().debug('Received reply: \'{}\''.format(r))

        # Clear the busy flag
        getLogger().debug('Unlocking device')
        self.busy.clear()

        return r

    def flush(self):
        """ Cleans the input buffer.

        Raises
        ------
        :class:`serial.SerialException`
            General serial connection error.
        """
        getLogger().info('Cleaning input buffer of {}'.format(self.serial_port))
        self.serial.reset_input_buffer()
        getLogger().debug('Device says: {}'.format(
            self.serial.readline().decode("utf-8").replace('\n', ' ').replace('\r', ''))
        )

    def apply_defaults(self):
        """ Applies the default output values.

        Raises
        ------
        :class:`ValueError`
           Invalid default parameters.

        :class:`SerialException`
            Serial communication error

        :class:`RuntimeError`
           Device busy for too long.
        """
        getLogger().info('Applying default settings')

        # Apply default analog outputs, might raise ValueError, SerialException or RuntimeError
        for f in self.analog_outputs:
            if f.active:
                self.set_analog_output(f.id, f.value)

        # Apply default digital outputs, might raise ValueError, SerialException or RuntimeError
        for f in self.digital_outputs:
            if f.active:
                self.set_digital_output(f.id, f.value)

        # Apply default switch states, might raise ValueError, SerialException or RuntimeError
        for f in self.switches:
            if f.active:
                self.set_switch(f.id, f.value)

    def read_inputs(self):
        """ Reads the analog and digital inputs of the
        Polarity Switcher.

        Raises
        ------
        :class:`RuntimeError`
           Device busy for too long.
        """

        # Read analog inputs
        for ai in self.analog_inputs:
            if ai.active:
                try:
                    getLogger().debug('Reading analog input {}: {}'.format(ai.id, ai.label))
                    resp = self.command(ai.serial_string)
                    ai.value = float(resp)
                    getLogger().debug('Analog input from channel {}: {}'.format(ai.id, ai.value))
                except (SerialException, ValueError) as e:
                    getLogger().error("{}: {}".format(type(e).__name__, e))
                    ai.value = float('NaN')

        # TODO: read digital inputs

    def set_analog_output(
            self,
            output_id: int,
            value: float
    ):
        """ Sets the analog output with ID
        :paramref:`~PolaritySwitcher.set_analog_output.output_id` to
        :paramref:`~PolaritySwitcher.set_analog_output.value` Volt.

        Parameters
        ----------
        output_id : int
            ID of the output to set

        value: float
            Analog voltage to be set, in Volt.

        Raises
        ------
        :class:`ValueError`
           Invalid parameters.

        :class:`SerialException`
            Serial communication error

        :class:`RuntimeError`
           Device busy for too long.
        """
        # Check output ID is valid
        if output_id < 0 or output_id > len(self.analog_outputs):
            raise ValueError('Invalid analog output ID {}'.format(output_id))

        # Check output channel is enabled
        if not self.analog_outputs[output_id].active:
            raise ValueError('Analog output {} not active'.format(output_id))

        # Check voltage value
        # TODO: check value appropriateness

        # Set the voltage, might raise SerialException or RuntimeError
        self.command(self.analog_outputs[output_id].get_serial_string(value))

        # No error: update the status and return
        self.analog_outputs[output_id].value = value

        # Log
        getLogger().info('Analog output {} ({}) set to {} V'.format(
            output_id,
            self.analog_outputs[output_id].label,
            value
        ))

    def set_digital_output(
            self,
            output_id: int,
            value: bool
    ):
        """ Sets the digital output with ID
        :paramref:`~PolaritySwitcher.set_analog_output.output_id` to the
        :paramref:`~PolaritySwitcher.set_analog_output.value` state.

        Parameters
        ----------
        output_id : int
            ID of the output to set

        value: bool
            Digital output state

        Raises
        ------
        :class:`ValueError`
           Invalid parameters.

        :class:`SerialException`
            Serial communication error

        :class:`RuntimeError`
           Device busy for too long.
        """
        # Check output ID is valid
        if output_id < 0 or output_id > len(self.digital_outputs):
            raise ValueError('Invalid digital output ID {}'.format(output_id))

        # Check output channel is enabled
        if not self.digital_outputs[output_id].active:
            raise ValueError('Digital output {} not active'.format(output_id))

        # Set the output state, might raise SerialException or RuntimeError
        self.command(self.digital_outputs[output_id].get_serial_string(value))

        # No error: update the status and return
        self.digital_outputs[output_id].value = value

        # Log
        getLogger().info('Digital output {} ({}) set to {}'.format(
            output_id,
            self.digital_outputs[output_id].label,
            int(value)
        ))

    def set_switch(
            self,
            output_id: int,
            value: bool
    ):
        """ Sets the switch with ID
        :paramref:`~PolaritySwitcher.set_analog_output.output_id` to the
        :paramref:`~PolaritySwitcher.set_analog_output.value` state.

        Parameters
        ----------
        output_id : int
            ID of the switch to set

        value: bool
            Polarity switch state

        Raises
        ------
        :class:`ValueError`
           Invalid parameters.

        :class:`SerialException`
            Serial communication error

        :class:`RuntimeError`
           Device busy for too long.
        """
        # Check switch ID is valid
        if output_id < 0 or output_id > len(self.switches):
            raise ValueError('Invalid switch ID {}'.format(output_id))

        # Check output channel is enabled
        if not self.switches[output_id].active:
            raise ValueError('Switch {} not active'.format(output_id))

        # Set the switch state, might raise SerialException or RuntimeError
        self.command(self.switches[output_id].get_serial_string(value))

        # No error: update the status and return
        self.switches[output_id].value = value

        # Log
        getLogger().info('Polarity switch {} ({}) set to {}'.format(
            output_id,
            self.switches[output_id].label,
            int(value)
        ))
