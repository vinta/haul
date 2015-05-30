# coding: utf-8

from __future__ import unicode_literals

from collections import OrderedDict
import mimetypes
import re

from bs4 import BeautifulSoup
import requests

from . import exceptions
from . import settings
from . import utils


simple_url_re = re.compile(r'^https?://\[?\w', re.IGNORECASE)


class Haul(object):
    """
    Haul
    """

    def __init__(self,
                 parser=settings.DEFAULT_PARSER,
                 extractor_pipeline=settings.EXTRACTOR_PIPELINE,
                 derivator_pipeline=settings.DERIVATOR_PIPELINE):

        self.parser = parser
        self.extractor_pipeline = extractor_pipeline
        self.derivator_pipeline = derivator_pipeline

        self.response = None  # via Requests
        self.soup = None  # via BeautifulSoup

        self._result = None

    def __repr__(self):
        return '<Haul [parser: %s]>' % (self.parser)

    @property
    def result(self):
        if not isinstance(self._result, HaulResult):
            self._result = HaulResult()

        return self._result

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

        real_url = r.url
        content = r.content

        try:
            content_type = r.headers['Content-Type']
        except KeyError:
            content_type, encoding = mimetypes.guess_type(real_url, strict=False)

        self.response = r

        return content_type.lower(), content

    def parse_html(self, html):
        """
        Use BeautifulSoup to parse HTML / XML
        http://www.crummy.com/software/BeautifulSoup/bs4/doc/#specifying-the-parser-to-use
        """

        soup = BeautifulSoup(html, self.parser)
        self.soup = soup

        title_tag = soup.find('title')
        self.result.title = title_tag.string if title_tag else None

        return soup

    def start_extractor_pipeline(self, *args, **kwargs):
        pipeline_input = {
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

        # remove unnecessary items
        pipeline_output.pop('pipeline_index', None)
        pipeline_output.pop('pipeline_break', None)
        pipeline_output.pop('soup', None)

        self.result.extractor_image_urls = pipeline_output.get('extractor_image_urls', [])

        return self.result

    def start_derivator_pipeline(self, *args, **kwargs):
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

        # remove unnecessary items
        pipeline_output.pop('pipeline_index', None)
        pipeline_output.pop('pipeline_break', None)
        pipeline_output.pop('extractor_image_urls', None)

        self.result.derivator_image_urls = pipeline_output.get('derivator_image_urls', [])

        return self.result

    # API
    def find_images(self, url_or_html, derive=False):
        url = None
        content = None

        try:
            is_url = simple_url_re.match(url_or_html)
        except TypeError:
            raise exceptions.InvalidParameterError('Should be a URL or HTML text')

        if is_url:
            url = url_or_html
            content_type, content = self.retrieve_url(url)
        else:
            content_type = 'text/html'
            content = url_or_html

        self.result.url = url
        self.result.content_type = content_type

        if 'text/html' in content_type:
            self.parse_html(content)
            self.start_extractor_pipeline()
            if derive:
                self.start_derivator_pipeline()
        elif 'image/' in content_type:
            self.result.extractor_image_urls = [str(self.response.url), ]
            if derive:
                self.start_derivator_pipeline()
        else:
            raise exceptions.ContentTypeNotSupported(content_type)

        return self.result


class HaulResult(object):
    """
    Retrieval result of Haul
    """

    def __init__(self):
        self.url = None
        self.content_type = None
        self.title = None
        self.extractor_image_urls = []
        self.derivator_image_urls = []

    def __repr__(self):
        return '<HaulResult [Content-Type: %s]>' % (self.content_type)

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

    def to_ordered_dict(self):
        order_keys = (
            'url',
            'content_type',
            'title',
            'extractor_image_urls',
            'derivator_image_urls',
        )

        d = OrderedDict()
        for key in order_keys:
            d[key] = getattr(self, key)

        return d
