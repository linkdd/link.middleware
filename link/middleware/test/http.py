# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock, patch
from unittest import main

from link.middleware.core import Middleware
from link.middleware.http import HTTPMiddleware


class TestHTTP(UTCase):
    def setUp(self):
        patcher = patch('link.middleware.http.requests')
        self.module = patcher.start()
        self.addCleanup(patcher.stop)

        self.mid = Middleware.get_middleware_by_uri('http://')

    def test_get(self):
        response = MagicMock()
        response.ok = True
        response.text = 'content'

        self.module.get = MagicMock(return_value=response)

        result = self.mid.get()

        self.module.get.assert_called_with('http://')
        self.assertEqual(result, response.text)

        response.ok = False

        with self.assertRaises(HTTPMiddleware.Error):
            self.mid.get()

    def test_post(self):
        response = MagicMock()
        response.ok = True
        response.text = 'content'
        data = 'data'

        self.module.post = MagicMock(return_value=response)

        result = self.mid.post(data)

        self.module.post.assert_called_with('http://', data=data)
        self.assertEqual(result, response.text)

        response.ok = False

        with self.assertRaises(HTTPMiddleware.Error):
            self.mid.post(data)

    def test_put(self):
        response = MagicMock()
        response.ok = True
        response.text = 'content'
        data = 'data'

        self.module.put = MagicMock(return_value=response)

        result = self.mid.put(data)

        self.module.put.assert_called_with('http://', data=data)
        self.assertEqual(result, response.text)

        response.ok = False

        with self.assertRaises(HTTPMiddleware.Error):
            self.mid.put(data)

    def test_delete(self):
        response = MagicMock()
        response.ok = True
        response.text = 'content'
        data = 'data'

        self.module.delete = MagicMock(return_value=response)

        result = self.mid.delete(data)

        self.module.delete.assert_called_with('http://', data=data)
        self.assertEqual(result, response.text)

        response.ok = False

        with self.assertRaises(HTTPMiddleware.Error):
            self.mid.delete(data)

    def test_patch(self):
        response = MagicMock()
        response.ok = True
        response.text = 'content'
        data = 'data'

        self.module.patch = MagicMock(return_value=response)

        result = self.mid.patch(data)

        self.module.patch.assert_called_with('http://', data=data)
        self.assertEqual(result, response.text)

        response.ok = False

        with self.assertRaises(HTTPMiddleware.Error):
            self.mid.patch(data)

    def test_options(self):
        response = MagicMock()
        response.ok = True
        response.text = 'content'
        response.headers = {
            'allow': ['GET', 'POST']
        }

        self.module.options = MagicMock(return_value=response)

        result = self.mid.options()

        self.module.options.assert_called_with('http://')
        self.assertEqual(result, response.headers['allow'])

        response.ok = False

        with self.assertRaises(HTTPMiddleware.Error):
            self.mid.options()

    def test_head(self):
        response = MagicMock()
        response.ok = True
        response.text = 'content'
        response.headers = {
            'allow': ['GET', 'POST']
        }

        self.module.head = MagicMock(return_value=response)

        result = self.mid.head()

        self.module.head.assert_called_with('http://')
        self.assertEqual(result, response.headers)

        response.ok = False

        with self.assertRaises(HTTPMiddleware.Error):
            self.mid.head()


if __name__ == '__main__':
    main()
