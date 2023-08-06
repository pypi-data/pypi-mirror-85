# mh_universal_functions

mh_universal_functions is a Python library currently used in Python programs pir.py and rha.py.
(see https://www.makeareadme.com/ for examples of README.md)


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install mh_universal_functions.

```bash
sudo /usr/local/bin/python3.7 -m pip install mh-universal-functions==version
```


## Usage

```python
import mh_universal_functions

mh_universal_functions.test() # returns 'Hello world of PyPI'
```

Included functions:
 - def database_update_universal(mysql_const, row, table, value, id1, id1_value, id2, id2_value)
 - def database_read(mysql_const, row, table, id1, id1_value, id2, id2_value)
 - def read_config(_config_filename, _program_name, _log_filename, _hostname)
 - def exit_critical(_program_name, _log_filename, _hostname)
 - def send_telegram_message(telegram_active, telegram_program, telegram_recipient_dict, telegram_message_address,
                             telegram_message, telegram_picture)
 - def test()


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)