# coding: utf-8

from __future__ import unicode_literals

import mimetypes

from bs4 import BeautifulSoup
import requests

from haul import exceptions
from haul import utils


class Config(object):

    def __init__(self):
        # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
        self.parser = 'html5lib'

        # http://www.sitepoint.com/web-foundations/mime-types-complete-list/
        self.allowed_content_types = [
            'text/html',
            'image/',
        ]

        self.extractor_pipeline = (
            'haul.extractors.pipeline.html.img_src_finder',
            'haul.extractors.pipeline.html.a_href_finder',
            'haul.extractors.pipeline.css.background_image_finder',
        )

        self.derivator_pipeline = (
            'haul.derivators.pipeline.google.blogspot_s1600_extender',
            'haul.derivators.pipeline.google.ggpht_s1600_extender',
            'haul.derivators.pipeline.google.googleusercontent_s1600_extender',
            'haul.derivators.pipeline.pinterest.original_image_extender',
            'haul.derivators.pipeline.wordpress.original_image_extender',
            'haul.derivators.pipeline.tumblr.media_1280_extender',
            'haul.derivators.pipeline.tumblr.avatar_128_extender',
        )

    def add_extract_pipline(self, custom_pipeline, override=False):
        pass


class Procedure(object):
    """
    The one who actually does the dirty work.
    """

    def __init__(self, url_or_html, derive, config):
        self.url_or_html = url_or_html
        self.derive = derive
        self.config = config

        self.result = Result()
        self.soup = None  # via BeautifulSoup

    def start(self):
        if utils.is_url(self.url_or_html):
            url = self.url_or_html
            content_type, content = self.retrieve_url(url)
        else:
            content_type = 'text/html'
            content = self.url_or_html

        self.result.content_type = content_type

        if '/html' in content_type:
            self.parse_html(content)

        self.start_extractor_pipeline()

        if self.derive:
            self.start_derivator_pipeline()

        return self.result

    def retrieve_url(self, url):
        """
        Use requests to fetch remote content
        """

        try:
            r = requests.get(url)
        except requests.ConnectionError:
            raise exceptions.RetrieveError('Connection fail')

        if r.status_code >= 400:
            raise exceptions.RetrieveError('Connected, but status code is %s' % (r.status_code))

        self.result.url = r.url
        content = r.content

        try:
            content_type = r.headers['Content-Type']
        except KeyError:
            content_type, encoding = mimetypes.guess_type(self.url, strict=False)
        finally:
            content_type = content_type.lower()

        return content_type, content

    def parse_html(self, html):
        """
        Use BeautifulSoup to parse HTML / XML
        http://www.crummy.com/software/BeautifulSoup/bs4/doc/#specifying-the-parser-to-use
        """

        self.soup = BeautifulSoup(html, self.config.parser)

        title_tag = self.soup.find('title')
        self.result.title = title_tag.string if title_tag else None

    def start_extractor_pipeline(self, *args, **kwargs):

        self.result.extractor_image_urls = [str(self.url), ]

        pipeline_input = {
            'procedure': self,
            'soup': self.soup,
        }
        pipeline_output = pipeline_input.copy()

        for idx, name in enumerate(self.extractor_pipeline):
            pipeline_output['pipeline_index'] = idx
            pipeline_output['pipeline_break'] = False

            if hasattr(name, '__call__'):
                finder_func = name
            else:
                finder_func = utils.module_member(name)

            output = finder_func(*args, **pipeline_output)

            if isinstance(output, dict):
                pipeline_output.update(output)

            if pipeline_output['pipeline_break']:
                break

        self.result.extractor_image_urls = pipeline_output.get('extractor_image_urls', [])

    def start_derivator_pipeline(self, *args, **kwargs):
        if not self.result.extractor_image_urls:
            return

        pipeline_input = {
            'extractor_image_urls': self.result.extractor_image_urls,
        }
        pipeline_output = pipeline_input.copy()

        for idx, name in enumerate(self.derivator_pipeline):
            pipeline_output['pipeline_index'] = idx
            pipeline_output['pipeline_break'] = False

            if hasattr(name, '__call__'):
                extender_func = name
            else:
                extender_func = utils.module_member(name)

            output = extender_func(*args, **pipeline_output)

            if isinstance(output, dict):
                pipeline_output.update(output)

            if pipeline_output['pipeline_break']:
                break

        self.result.derivator_image_urls = pipeline_output.get('derivator_image_urls', [])


class Result(object):
    """
    Retrieval result of Haul, it's just a container.
    """

    def __init__(self):
        self.url = None
        self.content_type = None
        self.title = None
        self.extractor_image_urls = []
        self.derivator_image_urls = []

    def __repr__(self):
        return '<Result [Content-Type: %s]>' % (self.content_type)

    @property
    def is_found(self):
        return True if len(self.extractor_image_urls) > 0 else False

    @property
    def image_urls(self):
        """
        Combine extractor_image_urls and derivator_image_urls,
        remove duplicate but keep order
        """

        all_image_urls = self.extractor_image_urls[:]
        for image_url in self.derivator_image_urls:
            if image_url not in all_image_urls:
                all_image_urls.append(image_url)

        return all_image_urls

    def to_dict(self):
        return self.__dict__


class Hauler(object):
    """
    The entry point.
    """

    def __init__(self, config=None):
        if not config:
            config = Config()

        self.config = config

    def haul(self, url_or_html, derive=False):
        process = Procedure(url_or_html, derive=derive, config=self.config)
        result = process.start()

        return result
