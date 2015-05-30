# coding: utf-8

import re


def original_image_extender(pipeline_index,
                            extractor_image_urls,
                            derivator_image_urls=[],
                            *args, **kwargs):
    """
    Example:
    http://fashion-fever.nl/wp-content/upload/2013/09/DSC_0058-110x110.jpg
    http://www.wendyslookbook.com/wp-content/uploads/2013/09/Morning-Coffee-Run-7-433x650.jpg
    to
    http://fashion-fever.nl/wp-content/upload/2013/09/DSC_0058.jpg
    http://www.wendyslookbook.com/wp-content/uploads/2013/09/Morning-Coffee-Run-7.jpg
    """

    now_derivator_image_urls = []

    check_re = re.compile(r'wp-content/uploads?/', re.IGNORECASE)
    search_re = re.compile(r'(\-\d+x\d+).', re.IGNORECASE)

    for image_url in extractor_image_urls:
        if check_re.search(image_url):
            if search_re.search(image_url):
                extender_image_url = search_re.sub('.', image_url)
                now_derivator_image_urls.append(extender_image_url)

    output = {}
    output['derivator_image_urls'] = derivator_image_urls + now_derivator_image_urls

    return output
