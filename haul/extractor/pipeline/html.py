# coding: utf-8

from haul.compat import str


def img_tag(procedure,
            extractor_image_urls,
            *args, **kwargs):
    """
    Extract image URLs from <img> tags.
    """

    attributes = ('src', 'data-src')
    for img in procedure.document.find_all('img'):
        for attribute in attributes:
            src = img.get(attribute, None)
            if src:
                src = str(src)
                if src not in extractor_image_urls:
                    extractor_image_urls.append(src)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls

    return output


def a_tag(procedure,
          extractor_image_urls,
          *args, **kwargs):
    """
    Extract image URLs from <a> tags
    """

    for a in procedure.document.find_all('a'):
        href = a.get('href', None)
        if href:
            href = str(href)
            if filter(href.lower().endswith, procedure.config.allowed_image_extensions):
                if href not in extractor_image_urls:
                    extractor_image_urls.append(href)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls

    return output


def meta_tag(procedure,
             extractor_image_urls,
             *args, **kwargs):
    """
    Extract image URLs from <meta> tags
    """

    for a in procedure.document.find_all('meta'):
        href = a.get('content', None)
        if href:
            href = str(href)
            if filter(href.lower().endswith, procedure.config.allowed_image_extensions):
                if href not in extractor_image_urls:
                    extractor_image_urls.append(href)

    output = {}
    output['extractor_image_urls'] = extractor_image_urls

    return output
