# coding: utf-8

"""
haul.compat
~~~~~~~~~~~

This module contains imports and declarations for seamless Python 2 and
Python 3 compatibility.
"""

import sys


_version = sys.version_info

is_py2 = (_version[0] == 2)
is_py3 = (_version[0] == 3)

if is_py2:
    from urlparse import urljoin, urlparse

    str = unicode

elif is_py3:
    from urllib.parse import urljoin, urlparse

    str = str
