# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock
from unittest import main

from link.middleware.connectable import ConnectableMiddleware


class TestConnectable(UTCase):
    def setUp(self):
        self.conn = 'conn'
        self.disconnect = MagicMock()
        self.mid = ConnectableMiddleware()
        self.mid._connect = MagicMock(return_value=self.conn)
        self.mid._disconnect = self.disconnect
        self.mid._isconnected = MagicMock(
            side_effect=lambda c: c is not None
        )

    def test_connect(self):
        self.assertIs(self.conn, self.mid.conn)
        self.mid.connect()

        self.mid._connect.assert_called_once_with()

    def test_isconnected(self):
        self.assertFalse(self.mid.isconnected())
        self.mid.connect()
        self.assertTrue(self.mid.isconnected())

    def test_disconnect(self):
        self.mid.connect()

        self.mid.disconnect()
        self.mid.disconnect()

        self.mid._disconnect.assert_called_once_with(self.conn)

    def test_del(self):
        self.mid.connect()
        del self.mid

        self.disconnect.assert_called_once_with(self.conn)


if __name__ == '__main__':
    main()
