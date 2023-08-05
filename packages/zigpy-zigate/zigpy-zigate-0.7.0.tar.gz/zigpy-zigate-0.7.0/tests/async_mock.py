"""Mock utilities that are async aware."""
import sys

if sys.version_info[:2] < (3, 8):
    from mock import *  # noqa
else:
    from unittest.mock import *  # noqa
