# coding: utf-8

import sys
sys.path.insert(0, '..')

import unittest

from haul import Haul, HaulResult
from haul import exceptions
from haul.utils import pp, read_file


class HaulBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.complete_html = read_file('fixtures/page.html')
        self.fragmented_html = read_file('fixtures/fragment.html')

        self.blogspot_html = read_file('fixtures/blogspot.html')
        self.tumblr_html = read_file('fixtures/tumblr.html')
        self.wordpress_html = read_file('fixtures/wordpress.html')

        self.webpage_url = 'http://vinta.ws/blog/529'

        self.image_url = 'http://files.heelsfetishism.com/media/heels/2013/09/01/16576_3ce9d1b8c1744319837bab454ed10f0d.jpg'
        self.image_url_with_querysting = 'http://files.heelsfetishism.com/media/heels/2013/08/20/2070_566cf1cd44fd4692aa6cca9b3408a97d.jpg?q=test'
        self.image_url_with_hashtag = 'http://files.heelsfetishism.com/media/heels/2013/08/20/2070_566cf1cd44fd4692aa6cca9b3408a97d.jpg#test'

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

        self.broken_url = 'http://heelsfetishism.com/404/not/found/'
        self.not_supported_url = 'https://www.youtube.com/audiolibrary_download?vid=463864fcafcbc5bc'


class FindImagesFromHTMLTestCase(HaulBaseTestCase):

    def setUp(self):
        super(FindImagesFromHTMLTestCase, self).setUp()

    def test_find_html_document(self):
        h = Haul()
        hr = h.find_images(self.complete_html)

        self.assertIsInstance(hr, HaulResult)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 5)

    def test_find_html_fragment(self):
        h = Haul()
        hr = h.find_images(self.fragmented_html)

        self.assertIsInstance(hr, HaulResult)

        image_urls = hr.image_urls
        image_urls_count = len(image_urls)
        self.assertEqual(image_urls_count, 5)


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

class PropagatorPipelineTestCase(HaulBaseTestCase):

    def setUp(self):
        super(PropagatorPipelineTestCase, self).setUp()

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


class ExceptionsTestCase(HaulBaseTestCase):

    def setUp(self):
        super(ExceptionsTestCase, self).setUp()

    def test_retrieve_error(self):
        h = Haul()

        with self.assertRaises(exceptions.RetrieveError):
            h.find_images(self.broken_url)

    def test_content_type_not_supported(self):
        h = Haul()

        with self.assertRaises(exceptions.ContentTypeNotSupported):
            h.find_images(self.not_supported_url)


if __name__ == '__main__':
    print 'testing Haul'
    unittest.main()
