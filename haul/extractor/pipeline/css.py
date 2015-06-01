# coding: utf-8

import cssutils

from haul import utils


# TODO: support external css file
def background_property(procedure,
                        extractor_image_urls,
                        *args, **kwargs):
    """
    Extract image URLs from background CSS property.
    """

    for tag in procedure.document.find_all(style=True):
        style_string = tag['style']
        if 'background' in style_string.lower():
            style = cssutils.parseStyle(style_string)
            background = style.getProperty('background')
            if background:
                for property_value in background.propertyValue:
                    background_image_url = str(property_value.value)
                    if utils.is_url(background_image_url):
                        if background_image_url not in extractor_image_urls:
                            extractor_image_urls.append(background_image_url)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls

    return output


def background_image_property(procedure,
                              extractor_image_urls,
                              *args, **kwargs):
    """
    Extract image URLs from background-image CSS property.
    """

    for tag in procedure.document.find_all(style=True):
        style_string = tag['style']
        if 'background-image' in style_string.lower():
            style = cssutils.parseStyle(style_string)
            background_image = style.getProperty('background-image')
            if background_image:
                for property_value in background_image.propertyValue:
                    background_image_url = str(property_value.value)
                    if background_image_url:
                        if background_image_url not in extractor_image_urls:
                            extractor_image_urls.append(background_image_url)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls

    return output
