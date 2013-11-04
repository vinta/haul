# coding: utf-8

import cStringIO
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


def pack_image(self, content):
    string_io = cStringIO.StringIO(content)

    return string_io
