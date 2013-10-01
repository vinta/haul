# coding: utf-8

from .models import Haul


def find_images(url_or_html, *args, **kwargs):
    h = Haul()

    return h.find_images(url_or_html, *args, **kwargs)
