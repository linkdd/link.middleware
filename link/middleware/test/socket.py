# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock, call
from unittest import main

from link.middleware.socket import SocketMiddleware


class TestSocket(UTCase):
    def setUp(self):
        self.sock = MagicMock()
        self.sock.close = MagicMock()

        self.mid = SocketMiddleware(hosts=[('host', 80)])
        self.mid.new_socket = MagicMock(return_value=self.sock)
        self.mid._send = MagicMock()
        self.mid._receive = MagicMock(return_value='content')

    def test_connect(self):
        self.mid.connect()

        self.mid.new_socket.assert_called_with('host', 80)
        self.assertItemsEqual(self.mid.conn, [self.sock])

    def test_disconnect(self):
        self.mid.connect()
        self.mid.disconnect()

        self.sock.close.assert_called_with()

    def test_send(self):
        self.mid.send('data')

        self.mid._send.assert_called_with(self.sock, 'data')

    def test_receive(self):
        result = self.mid.receive(7)

        self.mid._receive.assert_called_with(self.sock, 7)
        self.assertEqual(result, 'content')


class TestMultiSocket(UTCase):
    def setUp(self):
        self.sock1 = MagicMock()
        self.sock1.close = MagicMock()

        self.sock2 = MagicMock()
        self.sock2.close = MagicMock()

        self.mid = SocketMiddleware(hosts=[('host1', 80), ('host2', 80)])
        self.mid.new_socket = MagicMock(side_effect=[self.sock1, self.sock2])
        self.mid._send = MagicMock()
        self.mid._receive = MagicMock(side_effect=['content1', 'content2'])

    def test_connect(self):
        self.mid.connect()

        self.mid.new_socket.assert_has_calls([
            call('host1', 80),
            call('host2', 80)
        ])

    def test_disconnect(self):
        self.mid.connect()
        self.mid.disconnect()

        self.sock1.close.assert_called_with()
        self.sock2.close.assert_called_with()

    def test_send(self):
        self.mid.send('data')

        self.mid._send.assert_has_calls([
            call(self.sock1, 'data'),
            call(self.sock2, 'data')
        ])

    def test_receive(self):
        result = self.mid.receive(8)

        self.mid._receive.assert_has_calls([
            call(self.sock1, 8),
            call(self.sock2, 8)
        ])

        self.assertEqual(result, ['content1', 'content2'])


if __name__ == '__main__':
    main()
