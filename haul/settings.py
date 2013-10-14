# coding: utf-8

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
DEFAULT_PARSER = 'lxml'

ALLOWED_CONTENT_TYPES = [
    'text/html',
    'image/',
]

FINDER_PIPELINE = (
    'haul.finders.pipeline.html.img_src_finder',
    'haul.finders.pipeline.html.a_href_finder',
    'haul.finders.pipeline.css.background_image_finder',
)

EXTENDER_PIPELINE = (
    'haul.extenders.pipeline.google.blogspot_s1600_extender',
    'haul.extenders.pipeline.google.ggpht_s1600_extender',
    'haul.extenders.pipeline.google.googleusercontent_s1600_extender',
    'haul.extenders.pipeline.pinterest.original_image_extender',
    'haul.extenders.pipeline.wordpress.original_image_extender',
    'haul.extenders.pipeline.tumblr.media_1280_extender',
    'haul.extenders.pipeline.tumblr.avatar_128_extender',
)

SHOULD_JOIN_URL = True
