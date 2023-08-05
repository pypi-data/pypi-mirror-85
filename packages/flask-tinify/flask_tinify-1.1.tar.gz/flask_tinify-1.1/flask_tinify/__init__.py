from .extension import Tinify
from .client import Client
from .result_meta import ResultMeta
from .result import Result
from .source import Source
from .errors import *

__version__ = '1.0'

__all__ = [
    b'Tinify',
    b'Client',
    b'Result',
    b'ResultMeta',
    b'Source',
    b'Error',
    b'AccountError',
    b'ClientError',
    b'ServerError',
    b'ConnectionError'
]
