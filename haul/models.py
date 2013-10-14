# coding: utf-8

import mimetypes
import re

from bs4 import BeautifulSoup
import requests

from . import exceptions, settings, utils


simple_url_re = re.compile(r'^https?://\[?\w', re.IGNORECASE)


class Haul(object):
    """
    Haul
    """

    def __init__(self,
                 parser=settings.DEFAULT_PARSER,
                 finder_pipeline=settings.FINDER_PIPELINE,
                 extender_pipeline=settings.EXTENDER_PIPELINE):

        self.parser = parser
        self.finder_pipeline = finder_pipeline
        self.extender_pipeline = extender_pipeline

        self.response = None # via Requests
        self.soup = None # via BeautifulSoup

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

        title_tag = soup.find('title')
        self.result.title = title_tag.string if title_tag else None

        self.soup = soup

        return soup

    def start_finder_pipeline(self, *args, **kwargs):
        pipeline_input = {
            'soup': self.soup,
        }
        pipeline_output = pipeline_input.copy()

        for idx, name in enumerate(self.finder_pipeline):
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

        self.result.finder_image_urls = pipeline_output.get('finder_image_urls', [])

        return self.result

    def start_extender_pipeline(self, *args, **kwargs):
        pipeline_input = {
            'finder_image_urls': self.result.finder_image_urls,
        }
        pipeline_output = pipeline_input.copy()

        for idx, name in enumerate(self.extender_pipeline):
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
        pipeline_output.pop('finder_image_urls', None)

        self.result.extender_image_urls = pipeline_output.get('extender_image_urls', [])

        return self.result

    # API
    def find_images(self, url_or_html, extend=False):
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

            self.start_finder_pipeline()

            if extend:
                self.start_extender_pipeline()

        elif 'image/' in content_type:
            self.result.finder_image_urls = [str(self.response.url), ]

            if extend:
                self.start_extender_pipeline()

        else:
            raise exceptions.ContentTypeNotSupported(content_type)

        return self.result


class HaulResult(object):
    """
    Result of Haul
    """

    def __init__(self):
        self.content_type = None
        self.url = None
        self.title = None
        self.finder_image_urls = []
        self.extender_image_urls = []

    def __repr__(self):
        return '<HaulResult [Content-Type: %s]>' % (self.content_type)

    @property
    def image_urls(self):
        """
        Combine finder_image_urls and extender_image_urls,
        remove duplicate but keep order
        """

        all_image_urls = self.finder_image_urls[:]
        for image_url in self.extender_image_urls:
            if not utils.in_ignorecase(image_url, all_image_urls):
                all_image_urls.append(image_url)

        return all_image_urls

    def to_dict(self):
        return self.__dict__
