# coding: utf-8

from ...compat import str


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
            src = str(src)
            if (src not in finder_image_urls) and \
               (src not in now_finder_image_urls):
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
            href = str(href)
            if filter(href.lower().endswith, ('.jpg', '.jpeg', '.gif', '.png')):
              if (href not in finder_image_urls) and \
                 (href not in now_finder_image_urls):
                    now_finder_image_urls.append(href)

    output = {}
    output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

    return output
