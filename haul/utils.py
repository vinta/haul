# coding: utf-8

import cStringIO
import re
import sys


def import_module(name):
    __import__(name)

    return sys.modules[name]


def module_member(name):
    mod, member = name.rsplit('.', 1)
    module = import_module(mod)

    return getattr(module, member)


def read_file(path):
    with open (path, 'r') as f:
        content = f.read()

    return content


def pack_image(content):
    string_io = cStringIO.StringIO(content)

    return string_io


def is_url(text):
    # https://github.com/django/django/blob/master/django/core/validators.py#L45
    regex = re.compile(
            r'^((?:http|ftp)s?:)?//' # http://, https:// or //
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
            r'localhost|' # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # IP
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return bool(regex.match(text))


def normalize_url(text):
    if text[:2] == '//':
        text = 'http:' + text

    return text
