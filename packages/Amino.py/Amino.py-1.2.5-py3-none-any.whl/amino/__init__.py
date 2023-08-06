__title__ = 'Amino.py'
__author__ = 'Slimakoi'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2020 Slimakoi'
__version__ = '1.2.5'

from .acm import ACM
from .client import Client
from .sub_client import SubClient
from .lib.util import device, exceptions, headers, helpers, objects
from .socket import Callbacks, SocketHandler
from requests import get
from ujson import loads

if __version__ != loads(get("https://pypi.python.org/pypi/Amino.py/json").text)["info"]["version"]:
    print(exceptions.LibraryUpdateAvailable)
