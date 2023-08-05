from .extension import Tinify
from .client import Client
from .result_meta import ResultMeta
from .result import Result
from .source import Source
from .errors import *
from .version import __version__


__all__ = [
    b'Tinify',
    b'__version__',
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
