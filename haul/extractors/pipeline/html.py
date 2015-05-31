# coding: utf-8

from haul.compat import str


def img_src_finder(pipeline_index,
                   soup,
                   extractor_image_urls=[],
                   *args, **kwargs):
    """
    Find image URLs in <img>'s src attribute
    """

    now_extractor_image_urls = []

    for img in soup.find_all('img'):
        src = img.get('src', None)
        if src:
            src = str(src)
            if (src not in extractor_image_urls) and \
               (src not in now_extractor_image_urls):
                now_extractor_image_urls.append(src)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls + now_extractor_image_urls

    return output


def a_href_finder(pipeline_index,
                  soup,
                  extractor_image_urls=[],
                  *args, **kwargs):
    """
    Find image URLs in <a>'s href attribute
    """

    now_extractor_image_urls = []

    for a in soup.find_all('a'):
        href = a.get('href', None)
        if href:
            href = str(href)
            if filter(href.lower().endswith, ('.jpg', '.jpeg', '.gif', '.png')):
              if (href not in extractor_image_urls) and \
                 (href not in now_extractor_image_urls):
                    now_extractor_image_urls.append(href)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls + now_extractor_image_urls

    return output
