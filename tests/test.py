# coding: utf-8

import os
import unittest

from haul import Haul
from haul import HaulResult
from haul import exceptions
from haul import utils
from haul.utils import read_file


TESTS_DIR = os.path.abspath(os.path.join(__file__, '../'))


class HaulBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.complete_html = read_file(os.path.join(TESTS_DIR, 'fixtures/page.html'))
        self.no_image_html = read_file(os.path.join(TESTS_DIR, 'fixtures/no_image_page.html'))
        self.fragmented_html = read_file(os.path.join(TESTS_DIR, 'fixtures/fragment.html'))

        self.blogspot_html = read_file(os.path.join(TESTS_DIR, 'fixtures/blogspot.html'))
        self.tumblr_html = read_file(os.path.join(TESTS_DIR, 'fixtures/tumblr.html'))
        self.wordpress_html = read_file(os.path.join(TESTS_DIR, 'fixtures/wordpress.html'))

        self.webpage_url = 'http://vinta.ws/blog/529'

        self.image_url = 'http://files.heelsfetishism.com/media/heels/2013/09/01/16576_3ce9d1b8c1744319837bab454ed10f0d.jpg'
        self.image_url_with_querysting = 'http://files.heelsfetishism.com/media/heels/2013/08/20/2070_566cf1cd44fd4692aa6cca9b3408a97d.jpg?q=test'

        self.amazon_url = 'http://www.amazon.com/dp/B00C67CRRE/'
        self.blogspot_url = 'http://atlantic-pacific.blogspot.tw/2013/09/formulaic-dressing.html'
        self.blogspot_image_url = 'http://1.bp.blogspot.com/-S97wTYQKbrY/UkWukhKhTKI/AAAAAAAAJ0g/fcRDiqVC8Us/s898/aaPOP+001.jpg'
        self.fancy_url = 'http://fancy.com/things/307759676836021549/Patent-Leather-Heels-by-Jimmy-Choo'
        self.flickr_url = 'http://www.flickr.com/photos/blurri/4997760101/'
        self.instagram_url = 'http://instagram.com/p/YC9A5JQdrS/'
        self.pinterest_url = 'http://www.pinterest.com/pin/237987161531161351/'
        self.pinterest_image_url = 'http://media-cache-ec0.pinimg.com/736x/50/9b/bd/509bbd5c6543d473bc2b49befe75f4c6.jpg'
        self.tumblr_url = 'http://gibuloto.tumblr.com/post/62525699435/fuck-yeah'
        self.tumblr_image_url = 'http://31.media.tumblr.com/e199758fc69df7554e64772e970b4fe0/tumblr_ms446vqoA21qbrjcdo1_500.jpg'
        self.wordpress_url = 'http://www.wendyslookbook.com/2013/09/morning-coffee-run-tweed-jacket-watermark-plaid/'
        self.wordpress_image_url = 'http://www.wendyslookbook.com/wp-content/uploads/2013/09/Morning-Coffee-Run-7-433x650.jpg'

        self.not_exist_url = 'http://domain-not-exist-123.com/'
        self.broken_url = 'http://heelsfetishism.com/404/not/found/'
        self.not_supported_url = 'https://www.youtube.com/audiolibrary_download?vid=463864fcafcbc5bc'


class HaulUtilsTestCase(HaulBaseTestCase):

    def setUp(self):
        super(HaulUtilsTestCase, self).setUp()

    def test_is_url(self):
        true_urls = [
            'http://heelsfetishism.com/',
            'http://heelsfetishism.com/?q=123',
            'http://heelsfetishism.com/heels/20011/',
            'http://heelsfetishism.com/from/vimeo.com/',
            'http://s3-ap-northeast-1.amazonaws.com/files.heelsfetishism.com/中文.png',
            'http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not',
            'https://twitter.com/vinta',
            'google.com',
            'google.com/image.jpg',
        ]
        for url in true_urls:
            self.assertTrue(utils.is_url(url))

        false_urls = [
            'google',
            'path/to/dead/',
            '/another/path/to/dead/',
            '//files.heelsfetishism.com/media/heels/2013/10/29/18953_c62b070a4e98479998c3ab613a3be0a1.jpg',
        ]
        for url in false_urls:
            self.assertFalse(utils.is_url(url))

    def test_normalize_url(self):
        url = '//files.heelsfetishism.com/media/heels/2013/10/25/18510_6543374da5da4008908eaee2a07bbada.jpg'
        new_url = utils.normalize_url(url)

        self.assertEqual(new_url, 'http://files.heelsfetishism.com/media/heels/2013/10/25/18510_6543374da5da4008908eaee2a07bbada.jpg')


class HaulResultTestCase(HaulBaseTestCase):

    def setUp(self):
        super(HaulResultTestCase, self).setUp()

    def test_is_found_true(self):
        h = Haul()
        hr = h.find_images(self.complete_html)

        self.assertTrue(hr.is_found)

    def test_is_found_false(self):
        h = Haul()
        hr = h.find_images(self.no_image_html)

        self.assertFalse(hr.is_found)


class FindImagesFromHTMLTestCase(HaulBaseTestCase):

    def setUp(self):
        super(FindImagesFromHTMLTestCase, self).setUp()

    def test_find_html_document(self):
        h = Haul()
        hr = h.find_images(self.complete_html)

        self.assertIsInstance(hr, HaulResult)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 6)

    def test_find_html_fragment(self):
        h = Haul()
        hr = h.find_images(self.fragmented_html)

        self.assertIsInstance(hr, HaulResult)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 6)


class FindImagesFromURLTestCase(HaulBaseTestCase):

    def setUp(self):
        super(FindImagesFromURLTestCase, self).setUp()

    def test_find_html_url(self):
        h = Haul()
        hr = h.find_images(self.webpage_url)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('text/html', hr.content_type)

    def test_fancy_url(self):
        h = Haul()
        hr = h.find_images(self.fancy_url)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('text/html', hr.content_type)

    def test_find_image_url(self):
        h = Haul()
        hr = h.find_images(self.image_url)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('image/', hr.content_type)


class FinderPipelineTestCase(HaulBaseTestCase):

    def setUp(self):
        super(FinderPipelineTestCase, self).setUp()

    def test_background_finder(self):
        FINDER_PIPELINE = (
            'haul.finders.pipeline.css.background_finder',
        )

        h = Haul(finder_pipeline=FINDER_PIPELINE)
        hr = h.find_images(self.complete_html)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('text/html', hr.content_type)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 2)


class ExtenderPipelineTestCase(HaulBaseTestCase):

    def setUp(self):
        super(ExtenderPipelineTestCase, self).setUp()

    def test_blogspot(self):
        h = Haul()
        hr = h.find_images(self.blogspot_html, extend=True)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('text/html', hr.content_type)

    def test_tumblr(self):
        h = Haul()
        hr = h.find_images(self.tumblr_html, extend=True)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('text/html', hr.content_type)

    def test_pinterest_image_url(self):
        h = Haul()
        hr = h.find_images(self.pinterest_image_url, extend=True)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('image/', hr.content_type)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 2)

    def test_tumblr_image_url(self):
        h = Haul()
        hr = h.find_images(self.tumblr_image_url, extend=True)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('image/', hr.content_type)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 2)

    def test_wordpress(self):
        h = Haul()
        hr = h.find_images(self.wordpress_html, extend=True)

        self.assertIsInstance(hr, HaulResult)
        self.assertIn('text/html', hr.content_type)


class CustomFinderPipelineTestCase(HaulBaseTestCase):

    def setUp(self):
        super(CustomFinderPipelineTestCase, self).setUp()

    def test_find_html_document(self):
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

        FINDER_PIPELINE = (
            'haul.finders.pipeline.html.img_src_finder',
            'haul.finders.pipeline.html.a_href_finder',
            'haul.finders.pipeline.css.background_image_finder',
            img_data_src_finder,
        )

        h = Haul(finder_pipeline=FINDER_PIPELINE)
        hr = h.find_images(self.complete_html)

        self.assertIsInstance(hr, HaulResult)

        test_image_url = 'http://files.heelsfetishism.com/media/heels/2013/10/03/18099_307a62430fa045cc9b2124d16de63f33.jpg'
        self.assertIn(test_image_url, hr.finder_image_urls)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 7)


class ExceptionsTestCase(HaulBaseTestCase):

    def setUp(self):
        super(ExceptionsTestCase, self).setUp()

    def test_invalid_parameter_error(self):
        h = Haul()

        with self.assertRaises(exceptions.InvalidParameterError):
            url_or_html = None
            h.find_images(url_or_html)

    def test_retrieve_error(self):
        h = Haul()

        with self.assertRaises(exceptions.RetrieveError):
            h.find_images(self.not_exist_url)

        with self.assertRaises(exceptions.RetrieveError):
            h.find_images(self.broken_url)

    def test_content_type_not_supported(self):
        h = Haul()

        with self.assertRaises(exceptions.ContentTypeNotSupported):
            h.find_images(self.not_supported_url)


if __name__ == '__main__':
    unittest.main()
