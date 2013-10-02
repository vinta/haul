# coding: utf-8

DEFAULT_PARSER = 'lxml'

FINDER_PIPELINE = (
    'haul.finders.pipeline.html.img_src_finder',
    'haul.finders.pipeline.html.a_href_finder',
    'haul.finders.pipeline.css.background_image_finder',
)

PROPAGATOR_PIPELINE = (
    'haul.extenders.pipeline.google.blogspot_s1600_propagator',
    'haul.extenders.pipeline.google.ggpht_s1600_propagator',
    'haul.extenders.pipeline.google.googleusercontent_s1600_propagator',
    'haul.extenders.pipeline.pinterest.original_image_propagator',
    'haul.extenders.pipeline.wordpress.original_image_propagator',
    'haul.extenders.pipeline.tumblr.media_1280_propagator',
    'haul.extenders.pipeline.tumblr.avatar_128_propagator',
)
