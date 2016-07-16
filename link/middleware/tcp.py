# -*- coding: utf-8 -*-

from link.middleware.socket import SocketMiddleware
from link.middleware.core import register_middleware
import socket


@register_middleware
class TCPMiddleware(SocketMiddleware):
    """
    TCP socket middleware.
    """

    __protocols__ = ['tcp']

    def new_socket(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock

    def _send(self, sock, data):
        sock.send(data)

    def _receive(self, sock, bufsize):
        return sock.recv(bufsize)
