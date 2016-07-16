# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from unittest import main

from link.middleware.core import Middleware, register_middleware
from link.middleware.core import MIDDLEWARES_BY_PROTOCOLS
from link.middleware.core import MIDDLEWARES_BY_URL


class SuperDummy(Middleware):
    __protocols__ = ['super']


class Dummy(SuperDummy):
    __protocols__ = ['dummy']
    __constraints__ = [SuperDummy]


class TestMiddleware(UTCase):
    def test_01_register(self):
        result = register_middleware(SuperDummy)

        self.assertIs(result, SuperDummy)
        self.assertIn('super', MIDDLEWARES_BY_PROTOCOLS)
        self.assertIn(result, MIDDLEWARES_BY_PROTOCOLS['super'])

        result = register_middleware(Dummy)

        self.assertIs(result, Dummy)
        self.assertIn('dummy', MIDDLEWARES_BY_PROTOCOLS)
        self.assertIn(result, MIDDLEWARES_BY_PROTOCOLS['dummy'])

    def test_02_protocols(self):
        protocols = Dummy.protocols()
        self.assertEqual(protocols, ['super', 'dummy'])

        mids_super = Middleware.get_middlewares_by_protocols('super')
        self.assertEqual(mids_super, [SuperDummy, Dummy])

        mids_dummy = Middleware.get_middlewares_by_protocols('dummy')
        self.assertEqual(mids_dummy, [Dummy])

    def test_03_constraints(self):
        constraints = Dummy.constraints()
        self.assertEqual(constraints, [SuperDummy])

    def test_04_uri(self):
        uri = 'dummy+dummy://user:pwd@host:80/path?f=b&foo[]=bar&bar[]=baz'
        mid = Middleware.get_middleware_by_uri(uri)

        self.assertIn(uri, MIDDLEWARES_BY_URL)
        self.assertIs(mid, MIDDLEWARES_BY_URL[uri])


if __name__ == '__main__':
    main()
