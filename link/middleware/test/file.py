# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock, patch
from unittest import main

from link.middleware.core import Middleware
from link.middleware.file import FileMiddleware


class TestFile(UTCase):
    def setUp(self):
        patcher1 = patch('link.middleware.file.os.remove')
        patcher2 = patch('link.middleware.file.os.path.exists')
        patcher3 = patch('link.middleware.file.open')

        self.remove = patcher1.start()
        self.exists = patcher2.start()
        self.open = patcher3.start()

        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)
        self.addCleanup(patcher3.stop)

        self.exists.return_value = True

        self.file = MagicMock()
        self.file.__enter__ = MagicMock(return_value=self.file)
        self.file.__exit__ = MagicMock()
        self.file.read = MagicMock(return_value='content')
        self.file.write = MagicMock()

        self.open.return_value = self.file

        self.mid = Middleware.get_middleware_by_uri('file:///path')

    def test_get(self):
        result = self.mid.get()

        self.assertEqual(result, 'content')
        self.open.assert_called_with('/path')
        self.file.read.assert_called_with()

    def test_post(self):
        self.mid.post('data')

        self.open.assert_called_with('/path', 'a')
        self.file.write.assert_called_with('data')

    def test_put(self):
        self.mid.put('data')

        self.open.assert_called_with('/path', 'w')
        self.file.write.assert_called_with('data')

    def test_delete(self):
        self.mid.delete(None)

        self.exists.assert_called_with('/path')
        self.remove.assert_called_with('/path')


if __name__ == '__main__':
    main()
