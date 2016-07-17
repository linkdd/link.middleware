# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from mock import MagicMock, patch
from unittest import main

from link.middleware.udp import UDPMiddleware


class TestUDP(UTCase):
    def setUp(self):
        patcher1 = patch('link.middleware.udp.socket')
        self.module = patcher1.start()
        self.addCleanup(patcher1.stop)

        self.sock = MagicMock()
        self.sock.bind = MagicMock()
        self.sock.close = MagicMock()
        self.sock.sendto = MagicMock()
        self.sock.recvfrom = MagicMock(return_value='content')

        self.module.socket = MagicMock(return_value=self.sock)
        self.module.AF_INET = 'inet'
        self.module.SOCK_DGRAM = 'dgram'

        self.mid = UDPMiddleware(hosts=[('host', 80)])

    def test_connect(self):
        self.mid.connect()

        self.module.socket.assert_called_with('inet', 'dgram')
        self.sock.bind.assert_called_with(('host', 80))
        self.assertEqual(self.mid.conn, [self.sock])

    def test_disconnect(self):
        self.mid.connect()
        self.mid.disconnect()

        self.sock.close.assert_called_with()

    def test_send(self):
        self.mid.send('data', 'host2', 80)

        self.sock.sendto.assert_called_with('data', ('host2', 80))

    def test_receive(self):
        result = self.mid.receive(7)

        self.sock.recvfrom.assert_called_with(7)
        self.assertEqual(result, 'content')


if __name__ == '__main__':
    main()
