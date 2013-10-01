# coding: utf-8

"""
haul.exceptions
~~~~~~~~~~~~~~~

This module contains the set of Haul's exceptions.
"""


class RetrieveError(RuntimeError):
    """
    HTTP status code >= 400
    """


class ContentTypeNotSupported(Exception):
    """
    """
