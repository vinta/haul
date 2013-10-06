# coding: utf-8

"""
haul.exceptions
~~~~~~~~~~~~~~~

This module contains the set of Haul's exceptions.
"""


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
    Support: `text/html` and `image/`
    """

    def __init__(self, content_type):
        Exception.__init__(self)

        self.content_type = content_type

    def __repr__(self):
        return '<ContentTypeNotSupported [content_type: %s]>' % (self.content_type)
