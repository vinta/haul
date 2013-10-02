# coding: utf-8

import re


def media_1280_propagator(pipeline_index, finder_image_urls, *args, **kwargs):
    """
    Example:
    http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_250.png
    http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_500.png
    to
    http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_1280.png
    """

    pre_propagator_image_urls = kwargs.get('propagator_image_urls', [])
    now_propagator_image_urls = []

    search_re = re.compile(r'(tumblr_[a-zA-Z0-9_]+)_(\d+).', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'media.tumblr.com/' in image_url.lower():
            if search_re.search(image_url):
                propagator_image_url = search_re.sub(r'\1_1280.', image_url)
                now_propagator_image_urls.append(propagator_image_url)

    output = {}
    output['propagator_image_urls'] = pre_propagator_image_urls + now_propagator_image_urls

    return output


def avatar_128_propagator(pipeline_index, *args, **kwargs):
    """
    Example:
    http://25.media.tumblr.com/avatar_2909d6610c26_16.png
    to
    http://25.media.tumblr.com/avatar_2909d6610c26_128.png
    """

    finder_image_urls = kwargs.get('finder_image_urls', [])

    pre_propagator_image_urls = kwargs.get('propagator_image_urls', [])
    now_propagator_image_urls = []

    search_re = re.compile(r'(avatar_[a-zA-Z0-9_]+)_(\d+).', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'media.tumblr.com/' in image_url.lower():
            if search_re.search(image_url):
                propagator_image_url = search_re.sub(r'\1_128.', image_url)
                now_propagator_image_urls.append(propagator_image_url)

    output = {}
    output['propagator_image_urls'] = pre_propagator_image_urls + now_propagator_image_urls

    return output
