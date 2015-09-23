# coding: utf-8

import cssutils


def background_image_finder(pipeline_index,
                            soup,
                            finder_image_urls=None,
                            *args, **kwargs):
    """
    Find image URL in background-image

    Example:
    <div style="width: 100%; height: 100%; background-image: url(http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg);" class="Image iLoaded iWithTransition Frame" src="http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg"></div>
    to
    http://distilleryimage10.ak.instagram.com/bde04558a43b11e28e5d22000a1f979a_7.jpg
    """
    if finder_image_urls is None:
        finder_image_urls = []

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
                        if (background_image_url not in finder_image_urls) and \
                           (background_image_url not in now_finder_image_urls):
                            now_finder_image_urls.append(background_image_url)

    output = {}
    output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

    return output
