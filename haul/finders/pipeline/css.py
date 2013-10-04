# coding: utf-8

import cssutils

from haul.utils import in_ignorecase


def background_image_finder(pipeline_index,
                            soup,
                            finder_image_urls=[],
                            *args, **kwargs):
    """
    Find image URL in background-image

    Example:
    <div style="width: 100%; height: 100%; background-image: url(http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg);" class="Image iLoaded iWithTransition Frame" src="http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg"></div>
    to
    http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg
    """

    now_finder_image_urls = []

    for tag in soup.find_all(style=True):
        style_string = tag['style']
        if 'background-image' in style_string.lower():
            style = cssutils.parseStyle(style_string)
            background_image = style.getProperty('background-image')
            if background_image:
                for property_value in background_image.propertyValue:
                    background_image_url = str(property_value.value)
                    if background_image_url:
                        if (not in_ignorecase(background_image_url, finder_image_urls)) and \
                           (not in_ignorecase(background_image_url, now_finder_image_urls)):
                            now_finder_image_urls.append(background_image_url)

    output = {}
    output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

    return output
