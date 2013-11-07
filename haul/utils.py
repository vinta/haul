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
    # # https://github.com/django/django/blob/master/django/core/validators.py#L45
    # url_re = re.compile(
    #         r'^((?:http|ftp)s?:)?//' # http://, https:// or //
    #         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
    #         r'localhost|' # localhost
    #         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # IP
    #         r'(?::\d+)?' # optional port
    #         r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # return bool(url_re.match(text))

    # https://github.com/jsocol/bleach/blob/master/bleach/__init__.py#L44
    PROTOCOLS = [
        'http',
        'https',
    ]

    TLDS = """ac ad ae aero af ag ai al am an ao aq ar arpa as asia at au aw ax az
           ba bb bd be bf bg bh bi biz bj bm bn bo br bs bt bv bw by bz ca cat
           cc cd cf cg ch ci ck cl cm cn co com coop cr cu cv cx cy cz de dj dk
           dm do dz ec edu ee eg er es et eu fi fj fk fm fo fr ga gb gd ge gf gg
           gh gi gl gm gn gov gp gq gr gs gt gu gw gy hk hm hn hr ht hu id ie il
           im in info int io iq ir is it je jm jo jobs jp ke kg kh ki km kn kp
           kr kw ky kz la lb lc li lk lr ls lt lu lv ly ma mc md me mg mh mil mk
           ml mm mn mo mobi mp mq mr ms mt mu museum mv mw mx my mz na name nc ne
           net nf ng ni nl no np nr nu nz om org pa pe pf pg ph pk pl pm pn pr pro
           ps pt pw py qa re ro rs ru rw sa sb sc sd se sg sh si sj sk sl sm sn so
           sr st su sv sy sz tc td tel tf tg th tj tk tl tm tn to tp tr travel tt
           tv tw tz ua ug uk us uy uz va vc ve vg vi vn vu wf ws xn ye yt yu za zm
           zw""".split()

    TLDS.reverse()

    """
    TODO: support `//domain.com/whatever/path/image.jpg`
    """

    url_re = re.compile(
        r"""\(*  # Match any opening parentheses.
        \b(?<![@.])(?:(?:%s):/{0,3}(?:(?:\w+:)?\w+@)?)?  # http://
        ([\w-]+\.)+(?:%s)(?:\:\d+)?(?!\.\w)\b   # xx.yy.tld(:##)?
        (?:[/?][^\s\{\}\|\\\^\[\]`<>"]*)?
        # /path/zz (excluding "unsafe" chars from RFC 1738,
        # except for # and ~, which happen in practice)
        """ % (u'|'.join(PROTOCOLS), u'|'.join(TLDS)), re.IGNORECASE | re.VERBOSE | re.UNICODE)

    return bool(url_re.match(text))


def normalize_url(text):
    if text[:2] == '//':
        text = 'http:' + text

    return text
