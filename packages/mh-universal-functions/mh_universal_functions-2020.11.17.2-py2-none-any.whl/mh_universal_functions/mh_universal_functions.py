# Module                       : mh_universal_functions.py
# Related program              : None
# Author                       : MH
# Date                         : see _version.py
# Version                      : see _version.py
# Python Version, Mac OS X     : 3.7.7
# Python Version, Raspberry Pi : 3.7.7


# Issue Log
# None


# Required packages in PyCharm and Raspberry Pi:
# Name             Type              Mac-Version  Raspi-Version  Dependencies  VersionCheckCommand
# ----------------------------------------------------------------------------------------------------------------------
# pybluez          external            0.23         0.23         -             print(bluetooth.__version__)
# configparser     standard-library   3.7.7        3.7.7         -             -
# datetime         standard-library   3.7.7        3.7.7         -             -
# fritzconnection  external           1.3.4        0.23          -             print(bluetooth.__version__)
# logging          standard-library   3.7.7        3.7.7         -             -
# os               standard-library   3.7.7        3.7.7         -             -
# pymysql          external          0.10.1       0.10.1         -             print(pymysql.__version__)
# subprocess       standard-library   3.7.7        3.7.7         -             -
# sys              standard-library   3.7.7        3.7.7         -             print(sys.version)
# threading        standard-library   3.7.7        3.7.7         -             -

# Module "bluetooth": The PyBluez module allows Python code to access the host machine's Bluetooth resources.
# (https://github.com/pybluez/pybluez)
import bluetooth

# Module "configparser": Configuration file parser
# (https://docs.python.org/3.7/library/configparser.html#module-configparser)
from configparser import ConfigParser

# Module "datetime": Basic date and time types
# (https://docs.python.org/3.7/library/datetime.html#module-datetime)
from datetime import datetime

# Module "fritzconnection": Basic date and time types
# (https://pypi.org/project/fritzconnection/)
from fritzconnection import FritzConnection

# Module "logging": Logging facility for Python
# (https://docs.python.org/3.7/library/logging.html#module-logging)
import logging

# Module "os": Miscellaneous operating system interfaces
# (https://docs.python.org/3.7/library/os.html#module-os)
from os import path

# Module "pymysql": Python MySQL client library
# (https://pypi.org/project/PyMySQL)
# Using "pymysql" instead of MySQLdb which is limited to python2.7
from pymysql import connect

# Module "subprocess": Subprocess management
# (https://docs.python.org/3.7/library/subprocess.html#module-subprocess)
from subprocess import check_call

# Import general modules
# Module "sys": System-specific parameters and functions
# (https://docs.python.org/3.7/library/sys.html#module-sys)
from sys import platform

# Module "threading": Thread-based parallelism
# (https://docs.python.org/3.7/library/threading.html)
from threading import Thread

# Version information
from mh_universal_functions._version import __version__


# Setting up logging
module_logger = logging.getLogger('__name__')


def database_update_universal(mysql_const, row, table, value, id1, id1_value, id2, id2_value):
    """
    Database update operation on an existing MySQL database.
    :param mysql_const: list, contains the following data:
                              - active: boolean, access the database
                              - host: str, name of the server hosting the MySQL database
                              - database: str, name of the MySQL database
                              - user: str, name of the user of the MySQL database
                              - password: str, password of the user
    :param row: str, name of the row of the database table which is intended to be updated
    :param table: str, name of the table which row is intended to be updated
    :param value: str, value with which the row is intended to be updated
    :param id1: str, first identification of the table to be updated
    :param id1_value: str, first identification value of the table to be updated
    :param id2: str, second identification of the table to be updated
    :param id2_value: str, second identification value of the table to be updated
    :returns: bool, true if database was successfully updated
    """

    active = mysql_const[0]
    host = mysql_const[1]
    database = mysql_const[2]
    user = mysql_const[3]
    password = mysql_const[4]

    if not active:
        return False

    try:
        db_connection = connect(
            host=host,
            db=database,
            user=user, passwd=password
        )
        cursor = db_connection.cursor()
        sql_statement_part1 = "UPDATE " + table + " SET " + row + "='" + str(value) + "' WHERE " + id1 + "='" +\
                              str(id1_value) + "'"
        sql_statement_part2 = " AND " + id2 + "='" + str(id2_value) + "'"

        if id2 == "":
            sql_statement = sql_statement_part1
        else:
            sql_statement = sql_statement_part1 + sql_statement_part2

        module_logger.info("Update of table: '" + table + "' in database: '" + database +
                           "' using sql statement: '" + sql_statement + "'")

        cursor.execute(sql_statement)
        db_connection.commit()
        db_connection.close()
        return True
    except Exception as error_detail1:
        module_logger.error("Cannot connect do database, error_detail1 = '" + str(error_detail1) + "'")
        return False


# Database read operation from a MySQL database
def database_read(mysql_const, row, table, id1, id1_value, id2, id2_value):
    """
    Read from MySQL database.
    :param mysql_const: list, contains the following data:
                              - active: boolean, name of the server hosting the MySQL database
                              - host: str, name of the server hosting the MySQL database
                              - database: str, name of the MySQL database
                              - user: str, name of the user of the MySQL database
                              - password: str, password of the user
    :param row: str, row of the database to be read from
    :param table: str, table of the database to be read from
    :param id1: str, first identification of the table to be updated
    :param id1_value: str, first identification value of the table to be updated
    :param id2: str, second identification of the table to be updated
    :param id2_value: str, second identification value of the table to be updated
    :returns: value: various, value of selected database row entry

    Example queries:
    test1 = database_read("statusRha", "switch433", "", "", "", "")
    test2 = database_read("statusRha", "switch433", "systemCode", "11111", "unitCode", "2")
    test3 = database_read("motion_stream_text", "pir_controls", "pir_controls_id", "1", "", "")
    """

    active = mysql_const[0]
    host = mysql_const[1]
    database = mysql_const[2]
    user = mysql_const[3]
    password = mysql_const[4]

    if not active:
        return False

    try:
        db_connection = connect(
            host=host,
            db=database,
            user=user, passwd=password
        )
        cursor = db_connection.cursor()
        sql_statement_basis = "SELECT " + row + " FROM " + table
        id1_statement = id1 + " = " + id1_value
        id2_statement = id2 + " = " + id2_value
        if id1 is not "" and id2 is not "":
            sql_statement = sql_statement_basis + " WHERE " + id1_statement + " AND " + id2_statement
        elif id1 is "" and id2 is "":
            sql_statement = sql_statement_basis
        elif id1 is "":
            sql_statement = sql_statement_basis + " WHERE " + id2_statement
        elif id2 is "":
            sql_statement = sql_statement_basis + " WHERE " + id1_statement
        else:
            return "error"
        cursor.execute(sql_statement)
        value = cursor.fetchone()[0]
        db_connection.close()
        return value
    except Exception as error_detail1:
        module_logger.error("Cannot connect to MySQL database, error_detail2 = '" + str(error_detail1) + "'")
        return "error"


def read_config(_config_filename, _program_name, _log_filename, _hostname):
    """
    Reads the configuration file.
    :param _config_filename: str, name of the configuration file
    :param _program_name: str, name of this program
    :param _log_filename: str, name of the logfile
    :param _hostname: str, name of the host machine
    :returns: the configuration files object
    """

    module_logger.info("Configuration file: loading...")
    if not path.isfile(_config_filename):
        module_logger.critical("Program stopped: no configuration file found (expected is: '" +
                               _config_filename + "')")
        exit_critical(_program_name, _log_filename, _hostname)
    config = ConfigParser()
    config.optionxform = str
    config.read(_config_filename)
    return config


def exit_critical(_program_name, _log_filename, _hostname):
    """
    Stops the program with a message to the console.
    :param _program_name: str, name of this program
    :param _log_filename: str, name of the logfile
    :param _hostname: str, name of the host machine
    :returns: None
    """

    print(_program_name + " (@" + _hostname +
          "): CRITICAL: Program stopped - check logfile: '" +
          _log_filename + "'" + " (timestamp = " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ")")
    exit()


def send_telegram_message(telegram_active, telegram_program, telegram_recipient_dict, telegram_message_address,
                          telegram_message, telegram_picture):
    """
    Sends telegram text and picture messages.
    :param telegram_active: str, whether telegram sending shall be active, can be "YES" or "NO"
    :param telegram_program: str, path to the telegram script
    :param telegram_recipient_dict: dict, contains the dict of keywords and telegram recipients
    :param telegram_message_address: str, contains the keyword which defines the recipients of the telegram message_text
    :param telegram_message: str, message_text to be send via telegram
    :param telegram_picture: str, path to picture to be send via telegram
    :returns: bool, whether the telegram message_text was send
    """

    def send_telegram_message_function(_telegram_active, _telegram_program, _telegram_recipient_dict,
                                       _telegram_message_address, _telegram_message, _telegram_picture):
        if (platform == "linux" or platform == "linux2" or platform == "darwin") and (_telegram_active == "YES"):
            try:
                if _telegram_message_address == "Message2All":
                    for key in _telegram_recipient_dict:
                        telegram_recipient = _telegram_recipient_dict[key]
                        telegram_recipient_message = telegram_recipient + " " + _telegram_picture + " " +\
                            _telegram_message
                        check_call([_telegram_program, telegram_recipient_message], shell=False)
                elif _telegram_message_address == "Message2None":
                    module_logger.warning("Telegram message_text: '" + _telegram_message +
                                          "' was not send, as telegram messaging is set to: '" +
                                          _telegram_message_address + "'")
                    return False
                else:
                    telegram_recipient = _telegram_recipient_dict[_telegram_message_address]
                    telegram_recipient_message = telegram_recipient + " " + _telegram_picture + " " + _telegram_message
                    check_call([_telegram_program, telegram_recipient_message], shell=False)
                module_logger.info("Telegram message_text send: '" + _telegram_message + "'")

# ToDO: think about adding _telegram_message_address to above module_logger message...

                return True
            except Exception as error_detail3:
                module_logger.error("Telegram message_text send: failed, error_detail3 = '" + str(error_detail3) + "'")
                return False
        else:
            module_logger.warning("Telegram message_text: '" + _telegram_message +
                                  "' was not send, as telegram messaging is switched off")
            return False

    # Start process_switches thread
    telegram_message_thread = Thread(target=send_telegram_message_function, args=(telegram_active,
                                                                                  telegram_program,
                                                                                  telegram_recipient_dict,
                                                                                  telegram_message_address,
                                                                                  telegram_message,
                                                                                  telegram_picture))
    telegram_message_thread.start()


def get_mobile_device_presence(_wifi_devices_dict, _router_ip_address, _router_password,
                               _bluetooth_devices_dict,
                               _scan_for_device_type,
                               _calling_software):
    """
    Evaluates whether bluetooth of WiFi devices as listed in the _wifi_devices_dict can be detected
    :param: _wifi_devices_dict: dict, contains the wifi devices name and Mac address
    :param: _router_ip_address: string, contains the routers ip address
    :param: _router_password: string, contains the routers password
    :param: _bluetooth_devices_dict: dict, contains the bluetooth devices name and Mac address
    :param: _scan_for_device_type: string, contains the scan type "bluetooth" or "wifi"
    :param: _calling_software: string, contains the which software is calling this function "rha" or "pir"
    :returns: bool, device in dictionaries _wifi_devices_dict or  _bluetooth_devices_dict are present
    """

    def scan_bluetooth():
        if platform == "linux" or platform == "linux2":
            for key in iter(_bluetooth_devices_dict.keys()):
                device_present = bluetooth.lookup_name(str(_bluetooth_devices_dict[key]), timeout=5)
                if device_present is not None:
                    return key, True
            return None, False
        else:
            return None, False

    def scan_wifi():
        fritz_connection = FritzConnection(address=_router_ip_address, password=_router_password)
        host_numbers = fritz_connection.call_action('Hosts', 'GetHostNumberOfEntries')['NewHostNumberOfEntries']
        index = 0
        while index < host_numbers:
            host = fritz_connection.call_action('Hosts', 'GetGenericHostEntry', NewIndex=index)
            for key in iter(_wifi_devices_dict.keys()):
                device_present = _wifi_devices_dict[key]
                if (host['NewMACAddress'] == device_present) and (host['NewActive']):
                    return key, True
            index = index + 1
        return None, False

    def mobile_device_presence():
        bluetooth_key, bluetooth_bool = scan_bluetooth()
        wifi_key, wifi_bool = scan_wifi()
        if (_scan_for_device_type == "bluetooth") or (wifi_key is None):
            if _calling_software == "pir":
                return bluetooth_key, bluetooth_bool
            elif _calling_software == "rha":
                return bluetooth_bool
        elif (_scan_for_device_type == "wifi") or (bluetooth_key is None):
            if _calling_software == "pir":
                return wifi_key, wifi_bool
            elif _calling_software == "rha":
                return wifi_bool
        else:
            if _calling_software == "pir":
                return None, False
            elif _calling_software == "rha":
                return False

    return mobile_device_presence


def test():
    print("Hello world of PyPI")
