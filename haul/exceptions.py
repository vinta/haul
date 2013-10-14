# coding: utf-8

"""
haul.exceptions
~~~~~~~~~~~~~~~

This module contains the set of Haul's exceptions.
"""


class InvalidParameterError(Exception):
    """
    Invalid Parameter
    """

    def __init__(self, message):
        Exception.__init__(self)

        self.message = message

    def __repr__(self):
        return '<InvalidParameterError [message: %s]>' % (self.message)


class RetrieveError(RuntimeError):
    """
    Connection fail or HTTP status code >= 400
    """

    def __init__(self, message):
        RuntimeError.__init__(self)

        self.message = message

    def __repr__(self):
        return '<RetrieveError [message: %s]>' % (self.message)


class ContentTypeNotSupported(Exception):
    """
    ref: settings.ALLOWED_CONTENT_TYPES
    """

    def __init__(self, content_type):
        Exception.__init__(self)

        self.content_type = content_type

    def __repr__(self):
        return '<ContentTypeNotSupported [content_type: %s]>' % (self.content_type)
