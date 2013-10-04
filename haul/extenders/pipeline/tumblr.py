# coding: utf-8

import re


def media_1280_extender(pipeline_index,
                        finder_image_urls,
                        extender_image_urls=[],
                        *args, **kwargs):
    """
    Example:
    http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_250.png
    http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_500.png
    to
    http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_1280.png
    """

    now_extender_image_urls = []

    search_re = re.compile(r'(tumblr_[a-zA-Z0-9_]+)_(\d+).', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'media.tumblr.com/' in image_url.lower():
            if search_re.search(image_url):
                extender_image_url = search_re.sub(r'\1_1280.', image_url)
                now_extender_image_urls.append(extender_image_url)

    output = {}
    output['extender_image_urls'] = extender_image_urls + now_extender_image_urls

    return output


def avatar_128_extender(pipeline_index,
                        finder_image_urls,
                        extender_image_urls=[],
                        *args, **kwargs):
    """
    Example:
    http://25.media.tumblr.com/avatar_2909d6610c26_16.png
    to
    http://25.media.tumblr.com/avatar_2909d6610c26_128.png
    """

    now_extender_image_urls = []

    search_re = re.compile(r'(avatar_[a-zA-Z0-9_]+)_(\d+).', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'media.tumblr.com/' in image_url.lower():
            if search_re.search(image_url):
                extender_image_url = search_re.sub(r'\1_128.', image_url)
                now_extender_image_urls.append(extender_image_url)

    output = {}
    output['extender_image_urls'] = extender_image_urls + now_extender_image_urls

    return output
