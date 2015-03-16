Haul
====

.. image:: http://img.shields.io/travis/vinta/Haul.svg?style=flat-square
    :alt: Build Badge
    :target: https://travis-ci.org/vinta/Haul

.. image:: http://img.shields.io/coveralls/vinta/Haul.svg?style=flat-square
    :alt: Coverage Badge
    :target: https://coveralls.io/r/vinta/Haul?branch=master

.. image:: https://img.shields.io/pypi/v/haul.svg?style=flat-square
    :alt: Version Badge
    :target: https://pypi.python.org/pypi/haul

Haul is an extensible web crawler for extracting URLs of thumbnails and **original images** from any web page.

Demo
====

`Hauler on Heroku <http://hauler.herokuapp.com/>`_

Installation
============

on Ubuntu

.. code-block:: bash

    $ sudo apt-get install build-essential python-dev libxml2-dev libxslt1-dev
    $ pip install haul

on Mac OS X

.. code-block:: bash

    $ brew install libxml2 libxslt
    $ pip install haul

Is there a problem during installation? `It's probably caused by lxml. <http://lxml.de/installation.html>`_

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

There are two key concepts that are presented as pure Python functions in Haul: the `Extractor` and the `Extender`.

- **Extractors** are responsible for extracting image URLs from web pages.
- **Extenders** are used for extending URLs with some predefined rules.

Built-in Extractors
-------------------

``haul.finders.pipeline.html.img_src_finder``
+++++++++++++++++++++++++++++++++++++++++++

Extracting image URLs from every ``<img src="value">`` in web pages.

``haul.finders.pipeline.html.a_href_finder``
++++++++++++++++++++++++++++++++++++++++++

Extracting image URLs from every ``<a href="value">`` in web pages.

``haul.finders.pipeline.css.background_image_finder``
+++++++++++++++++++++++++++++++++++++++++++++++++++

Extracting image URLs from every ``background-image: value`` or ``background: value``  in CSS.

Built-in Extenders
------------------

123

Custom finder or extender pipeline
----------------------------------

.. code-block:: python

    from haul import Haul
    from haul.compat import str


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
                src = str(src)
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

    $ python setup.py test
