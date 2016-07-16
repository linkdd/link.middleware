# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from unittest import main

from link.middleware.core import Middleware, register_middleware
from link.middleware.core import MIDDLEWARES_BY_PROTOCOLS
from link.middleware.core import MIDDLEWARES_BY_URL

from six.moves.urllib.parse import urlsplit, parse_qsl


class SuperDummy(Middleware):
    __protocols__ = ['super']


class Dummy(SuperDummy):
    __protocols__ = ['dummy']
    __constraints__ = [SuperDummy]

    def __init__(self, foo=None, bar=None, *args, **kwargs):
        super(Dummy, self).__init__(*args, **kwargs)

        self.foo = foo
        self.bar = bar


class NotSoDummy(Middleware):
    __protocols__ = ['notsodummy']


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

        result = register_middleware(NotSoDummy)

        self.assertIs(result, NotSoDummy)
        self.assertIn('notsodummy', MIDDLEWARES_BY_PROTOCOLS)
        self.assertIn(result, MIDDLEWARES_BY_PROTOCOLS['notsodummy'])

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
        uri = 'dummy://user@host,host2:80/path/subpath'
        mid = Middleware.get_middleware_by_uri(uri)

        self.assertEqual(mid.user, 'user')
        self.assertEqual(mid.pwd, None)
        self.assertEqual(mid.hosts, [('host', None), ('host2', 80)])
        self.assertEqual(mid.path, ['path', 'subpath'])

        uri = 'dummy://host:80,host2:80/path/subpath'
        mid = Middleware.get_middleware_by_uri(uri)

        self.assertEqual(mid.user, None)
        self.assertEqual(mid.pwd, None)
        self.assertEqual(mid.hosts, [('host', 80), ('host2', 80)])
        self.assertEqual(mid.path, ['path', 'subpath'])

    def test_05_uri_child(self):
        uri = 'dummy+dummy://user:pwd@host:80/path?f=b&foo=bar&bar=baz&foo=biz'
        mid = Middleware.get_middleware_by_uri(uri)

        self.assertIn(uri, MIDDLEWARES_BY_URL)
        self.assertIs(mid, MIDDLEWARES_BY_URL[uri])

        self.assertEqual(mid.user, 'user')
        self.assertEqual(mid.pwd, 'pwd')
        self.assertEqual(mid.hosts, [('host', 80)])
        self.assertEqual(mid.path, ['path'])
        self.assertEqual(mid.foo, ['bar', 'biz'])
        self.assertEqual(mid.bar, 'baz')

        child = mid.get_child_middleware()

        self.assertIsInstance(child, Dummy)

        self.assertEqual(child.user, 'user')
        self.assertEqual(child.pwd, 'pwd')
        self.assertEqual(child.hosts, [('host', 80)])
        self.assertEqual(child.path, ['path'])
        self.assertEqual(child.foo, ['bar', 'biz'])
        self.assertEqual(child.bar, 'baz')

        with self.assertRaises(Middleware.Error):
            mid.set_child_middleware(NotSoDummy())

    def test_06_uri_fail(self):
        with self.assertRaises(Middleware.Error):
            Middleware.get_middleware_by_uri('dumy://')

        with self.assertRaises(Middleware.Error):
            Middleware.get_middleware_by_uri('dummy+notsodummy://')

    def test_07_uri_cache(self):
        uri = 'dummy+dummy://user:pwd@hostname:80/path?f=b&foo=bar&bar=baz'
        self.assertNotIn(uri, MIDDLEWARES_BY_URL)

        mid = Middleware.get_middleware_by_uri(uri)
        self.assertIn(uri, MIDDLEWARES_BY_URL)
        self.assertIs(mid, MIDDLEWARES_BY_URL[uri])

        mid2 = Middleware.get_middleware_by_uri(uri)
        self.assertIs(mid, mid2)

    def test_08_tourl(self):
        uri = 'dummy://user:pwd@host:80/path?foo=bar'
        mid = Middleware.get_middleware_by_uri(uri)
        result = mid.tourl()

        self.assertEqual(uri, result)

    def test_09_tourl_nocache(self):
        uris = [
            'dummy://host:80/path?foo=bar&bar=baz&foo=biz',
            'dummy://user:pwd@host:80/path?foo=bar&bar=baz&foo=biz',
            'dummy://user@host/path?foo=bar&bar=baz&foo=biz',
            'dummy://user@host,host2:80/path?foo=bar&bar=baz&foo=biz'
        ]

        for uri in uris:
            mid = Middleware.get_middleware_by_uri(uri, cache=False)
            result = mid.tourl()

            parseduri = urlsplit(uri)
            parsedres = urlsplit(result)

            parseduri_query = parse_qsl(parseduri.query)
            parsedres_query = parse_qsl(parsedres.query)

            self.assertEqual(parseduri.scheme, parsedres.scheme)
            self.assertEqual(parseduri.username, parsedres.username)
            self.assertEqual(parseduri.password, parsedres.password)
            self.assertEqual(parseduri.hostname, parsedres.hostname)
            self.assertEqual(parseduri.port, parsedres.port)
            self.assertEqual(parseduri.path, parsedres.path)

            self.assertItemsEqual(parseduri_query, parsedres_query)


if __name__ == '__main__':
    main()
