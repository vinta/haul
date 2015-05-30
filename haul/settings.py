# coding: utf-8

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
DEFAULT_PARSER = 'lxml'

ALLOWED_CONTENT_TYPES = [
    'text/html',
    'image/',
]

EXTRACTOR_PIPELINE = (
    'haul.extractors.pipeline.html.img_src_finder',
    'haul.extractors.pipeline.html.a_href_finder',
    'haul.extractors.pipeline.css.background_image_finder',
)

DERIVATOR_PIPELINE = (
    'haul.derivators.pipeline.google.blogspot_s1600_extender',
    'haul.derivators.pipeline.google.ggpht_s1600_extender',
    'haul.derivators.pipeline.google.googleusercontent_s1600_extender',
    'haul.derivators.pipeline.pinterest.original_image_extender',
    'haul.derivators.pipeline.wordpress.original_image_extender',
    'haul.derivators.pipeline.tumblr.media_1280_extender',
    'haul.derivators.pipeline.tumblr.avatar_128_extender',
)

SHOULD_JOIN_URL = True
