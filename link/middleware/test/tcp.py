# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock, patch
from unittest import main

from link.middleware.tcp import TCPMiddleware


class TestTCP(UTCase):
    def setUp(self):
        patcher1 = patch('link.middleware.tcp.socket')
        self.module = patcher1.start()
        self.addCleanup(patcher1.stop)

        self.sock = MagicMock()
        self.sock.connect = MagicMock()
        self.sock.close = MagicMock()
        self.sock.send = MagicMock()
        self.sock.recv = MagicMock(return_value='content')

        self.module.socket = MagicMock(return_value=self.sock)
        self.module.AF_INET = 'inet'
        self.module.SOCK_STREAM = 'stream'

        self.mid = TCPMiddleware(hosts=[('host', 80)])

    def test_connect(self):
        self.mid.connect()

        self.module.socket.assert_called_with('inet', 'stream')
        self.sock.connect.assert_called_with(('host', 80))
        self.assertEqual(self.mid.conn, [self.sock])

    def test_disconnect(self):
        self.mid.connect()
        self.mid.disconnect()

        self.sock.close.assert_called_with()

    def test_send(self):
        self.mid.send('data')

        self.sock.send.assert_called_with('data')

    def test_receive(self):
        result = self.mid.receive(7)

        self.sock.recv.assert_called_with(7)
        self.assertEqual(result, 'content')


if __name__ == '__main__':
    main()
