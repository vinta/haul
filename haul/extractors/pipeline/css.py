# coding: utf-8

import cssutils

from haul import utils


def background_finder(pipeline_index,
                      soup,
                      extractor_image_urls=[],
                      *args, **kwargs):
    """
    Find image URL in background-image

    Example:
    <div style="background: #ffffff url('http://files.heelsfetishism.com/media/heels/2013/11/07/19822_eb071c1a5eb643818f6faa02f55b408f.jpg') no-repeat right top;" class="Image iLoaded iWithTransition Frame" src="http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg"></div>
    to
    http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg
    """

    now_extractor_image_urls = []

    for tag in soup.find_all(style=True):
        style_string = tag['style']
        if 'background' in style_string.lower():
            style = cssutils.parseStyle(style_string)
            background = style.getProperty('background')
            if background:
                for property_value in background.propertyValue:
                    background_image_url = str(property_value.value)
                    if utils.is_url(background_image_url):
                        if (background_image_url not in extractor_image_urls) and \
                           (background_image_url not in now_extractor_image_urls):
                            now_extractor_image_urls.append(background_image_url)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls + now_extractor_image_urls

    return output


def background_image_finder(pipeline_index,
                            soup,
                            extractor_image_urls=[],
                            *args, **kwargs):
    """
    Find image URL in background-image

    Example:
    <div style="width: 100%; height: 100%; background-image: url(http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg);" class="Image iLoaded iWithTransition Frame" src="http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg"></div>
    to
    http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg
    """

    now_extractor_image_urls = []

    for tag in soup.find_all(style=True):
        style_string = tag['style']
        if 'background-image' in style_string.lower():
            style = cssutils.parseStyle(style_string)
            background_image = style.getProperty('background-image')
            if background_image:
                for property_value in background_image.propertyValue:
                    background_image_url = str(property_value.value)
                    if background_image_url:
                        if (background_image_url not in extractor_image_urls) and \
                           (background_image_url not in now_extractor_image_urls):
                            now_extractor_image_urls.append(background_image_url)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls + now_extractor_image_urls

    return output
