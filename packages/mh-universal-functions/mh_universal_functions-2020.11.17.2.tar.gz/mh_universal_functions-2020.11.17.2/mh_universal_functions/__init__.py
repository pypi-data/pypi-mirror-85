# Module                       : __init__.py
# Related program              : mh_universal_functions.py
# Author                       : MH
# Date                         : see _version.py
# Version                      : see _version.py
# Python Version, Mac OS X     : 3.7.7
# Python Version, Raspberry Pi : 3.7.7


__all__ = ['database_update_universal',
           'database_read',
           'read_config',
           'exit_critical',
           'send_telegram_message',
           'get_mobile_device_presence',
           'test']

from .mh_universal_functions import *
from ._version import __version__
