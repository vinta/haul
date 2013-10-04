# coding: utf-8

from haul.utils import in_ignorecase


def img_src_finder(pipeline_index,
                   soup,
                   finder_image_urls=[],
                   *args, **kwargs):
    """
    Find image URL in <img>'s src attribute
    """

    now_finder_image_urls = []

    for img in soup.find_all('img'):
        src = img.get('src', None)
        if src:
            if (not in_ignorecase(src, finder_image_urls)) and \
               (not in_ignorecase(src, now_finder_image_urls)):
                now_finder_image_urls.append(src)

    output = {}
    output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

    return output


def a_href_finder(pipeline_index,
                  soup,
                  finder_image_urls=[],
                  *args, **kwargs):
    """
    Find image URL in <a>'s href attribute
    """

    now_finder_image_urls = []

    for a in soup.find_all('a'):
        href = a.get('href', None)
        if href:
            if filter(href.lower().endswith, ('.jpg', '.jpeg', '.gif', '.png')):
                if (not in_ignorecase(href, finder_image_urls)) and \
                   (not in_ignorecase(href, now_finder_image_urls)):
                    now_finder_image_urls.append(href)

    output = {}
    output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

    return output
