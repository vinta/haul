.. image:: https://d2weczhvl823v0.cloudfront.net/vinta/haul/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

Haul
====

Find thumbnails and original images from URL or HTML file.

Installation
============

on Ubuntu

.. code-block:: bash

    $ sudo apt-get install build-essential python-dev libxml2-dev libxslt1-dev
    $ pip install haul

on Mac OS X

.. code-block:: bash

    $ pip install haul

Fail to install haul? `It is probably caused by lxml <http://lxml.de/installation.html>`_.

Usage
=====

Find images from ``img src``, ``a href`` and even ``background-image``:

.. code-block:: python

    import haul

    url = 'http://gibuloto.tumblr.com/post/62525699435/fuck-yeah'
    result = haul.find_images(url)

    print(result.image_urls)
    """
    output:
    [
        'http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_500.png',
        ...
        'http://24.media.tumblr.com/avatar_a3a119b674e2_16.png',
        'http://25.media.tumblr.com/avatar_9b04f54875e1_16.png',
        'http://31.media.tumblr.com/avatar_0acf8f9b4380_16.png',
    ]
    """

Find original (or bigger size) images with ``extend=True``:

.. code-block:: python

    import haul

    url = 'http://gibuloto.tumblr.com/post/62525699435/fuck-yeah'
    result = haul.find_images(url, extend=True)

    print(result.image_urls)
    """
    output:
    [
        'http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_500.png',
        ...
        'http://24.media.tumblr.com/avatar_a3a119b674e2_16.png',
        'http://25.media.tumblr.com/avatar_9b04f54875e1_16.png',
        'http://31.media.tumblr.com/avatar_0acf8f9b4380_16.png',
        # bigger size, extended from above urls
        'http://25.media.tumblr.com/3f5f10d7216f1dd5eacb5eb3e302286a/tumblr_mtpcwdzKBT1qh9n5lo1_1280.png',
        ...
        'http://24.media.tumblr.com/avatar_a3a119b674e2_128.png',
        'http://25.media.tumblr.com/avatar_9b04f54875e1_128.png',
        'http://31.media.tumblr.com/avatar_0acf8f9b4380_128.png',
    ]
    """

Advanced Usage
==============

Custom finder / extender pipeline:

.. code-block:: python

    from haul import Haul
    from haul.utils import in_ignorecase


    def img_data_src_finder(pipeline_index,
                            soup,
                            finder_image_urls=[],
                            *args, **kwargs):
        """
        Find image URL in <img>'s data-src attribute
        """

        now_finder_image_urls = []

        for img in soup.find_all('img'):
            src = img.get('data-src', None)
            if src:
                if (not in_ignorecase(src, finder_image_urls)) and \
                   (not in_ignorecase(src, now_finder_image_urls)):
                    now_finder_image_urls.append(src)

        output = {}
        output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

        return output

    MY_FINDER_PIPELINE = (
        'haul.finders.pipeline.html.img_src_finder',
        'haul.finders.pipeline.css.background_image_finder',
        img_data_src_finder,
    )

    GOOGLE_SITES_EXTENDER_PIEPLINE = (
        'haul.extenders.pipeline.google.blogspot_s1600_extender',
        'haul.extenders.pipeline.google.ggpht_s1600_extender',
        'haul.extenders.pipeline.google.googleusercontent_s1600_extender',
    )

    url = 'http://fashion-fever.nl/dressing-up/'
    h = Haul(parser='lxml',
             finder_pipeline=MY_FINDER_PIPELINE,
             extender_pipeline=GOOGLE_SITES_EXTENDER_PIEPLINE)
    result = h.find_images(url, extend=True)

Run Tests
=========

.. code-block:: bash

    $ cd tests
    $ python test.py
