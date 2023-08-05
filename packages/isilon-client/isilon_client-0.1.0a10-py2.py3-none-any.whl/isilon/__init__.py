import logging
import os

from isilon.__version__ import __version__

logging.getLogger("isilon-client").addHandler(logging.NullHandler())
