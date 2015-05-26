# coding: utf-8

import re


def blogspot_s1600_extender(pipeline_index,
                            finder_image_urls,
                            extender_image_urls=[],
                            *args, **kwargs):
    """
    Example:
    http://1.bp.blogspot.com/-S97wTYQKbrY/UkWukhKhTKI/AAAAAAAAJ0g/fcRDiqVC8Us/s898/aaPOP+001.jpg
    to
    http://1.bp.blogspot.com/-S97wTYQKbrY/UkWukhKhTKI/AAAAAAAAJ0g/fcRDiqVC8Us/s1600/aaPOP+001.jpg
    """

    now_extender_image_urls = []

    search_re = re.compile(r'/s\d+/', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'bp.blogspot.com/' in image_url.lower():
            if search_re.search(image_url):
                extender_image_url = search_re.sub('/s1600/', image_url)
                now_extender_image_urls.append(extender_image_url)

    output = {}
    output['extender_image_urls'] = extender_image_urls + now_extender_image_urls

    return output


def ggpht_s1600_extender(pipeline_index,
                         finder_image_urls,
                         extender_image_urls=[],
                         *args, **kwargs):
    """
    Example:
    http://lh4.ggpht.com/-fFi-qJRuxeY/UjwHSOTHGOI/AAAAAAAArgE/SWTMT-hXzB4/s640/Celeber-ru-Emma-Watson-Net-A-Porter-The-Edit-Magazine-Photoshoot-2013-01.jpg
    to
    http://lh4.ggpht.com/-fFi-qJRuxeY/UjwHSOTHGOI/AAAAAAAArgE/SWTMT-hXzB4/s1600/Celeber-ru-Emma-Watson-Net-A-Porter-The-Edit-Magazine-Photoshoot-2013-01.jpg
    """

    now_extender_image_urls = []

    search_re = re.compile(r'/s\d+/', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'ggpht.com/' in image_url.lower():
            if search_re.search(image_url):
                extender_image_url = search_re.sub('/s1600/', image_url)
                now_extender_image_urls.append(extender_image_url)

    output = {}
    output['extender_image_urls'] = extender_image_urls + now_extender_image_urls

    return output


def googleusercontent_s1600_extender(pipeline_index,
                                     finder_image_urls,
                                     extender_image_urls=[],
                                     *args, **kwargs):
    """
    Example:
    https://lh6.googleusercontent.com/-T6V-utZHzbE/Ukjn-1MDOSI/AAAAAAAAA3g/H6Qcw1zt4n0/w555-h399-no/2101_aa2cac09d1c6431b8a635d61cd9c4471.jpg
    to
    https://lh6.googleusercontent.com/-T6V-utZHzbE/Ukjn-1MDOSI/AAAAAAAAA3g/H6Qcw1zt4n0/s1600/2101_aa2cac09d1c6431b8a635d61cd9c4471.jpg
    """

    now_extender_image_urls = []

    search_re = re.compile(r'/w\d+\-h\d+\-no/', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'googleusercontent.com/' in image_url.lower():
            if search_re.search(image_url):
                extender_image_url = search_re.sub('/s1600/', image_url)
                now_extender_image_urls.append(extender_image_url)

    output = {}
    output['extender_image_urls'] = extender_image_urls + now_extender_image_urls

    return output
