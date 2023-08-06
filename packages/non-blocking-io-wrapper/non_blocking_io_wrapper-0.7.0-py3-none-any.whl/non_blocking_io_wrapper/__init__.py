#  Copyright (c) 2020 SBA - MIT License

try:
    from .version import version as __version__
except ImportError:
    __version__ = '0.0.0'

from .non_blocking_reader import NonBlockingReader
