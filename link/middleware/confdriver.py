# -*- coding: utf-8 -*-

from b3j0f.conf.driver.base import ConfDriver
from b3j0f.conf import Parameter

from link.middleware.connectable import ConnectableMiddleware
from link.middleware.core import Middleware

from six import string_types
import json


class ConfDriver(ConfDriver):
    """
    Driver that reads configuration from a middleware.

    :param middleware: Middleware to read configuration from (or its URI)
    :type middleware: str or Middleware
    """

    def __init__(self, middleware, *args, **kwargs):
        super(ConfDriver, self).__init__(*args, **kwargs)

        if isinstance(middleware, string_types):
            middleware = Middleware.get_middleware_by_uri(middleware)

        if not isinstance(middleware, Middleware):
            raise TypeError(
                'Configuration driver expecting a Middleware, got: {0}'.format(
                    type(middleware)
                )
            )

        self.middleware = middleware

    def __del__(self):
        if isinstance(self.middleware, ConnectableMiddleware):
            self.middleware.disconnect()

    def rscpaths(self, path):
        return [path]

    def resource(self):
        return {}

    def _pathresource(self, rscpath):
        result = self.middleware.get(rscpath)

        if isinstance(result, string_types):
            result = json.loads(result)

        return result

    def _cnames(self, resource):
        return resource.keys()

    def _params(self, resource, cname):
        params = resource[cname]

        return [
            Parameter(name=key, svalue=params[key]) for key in params
        ]

    def _setconf(self, conf, resource, rscpath):
        for category in conf.values():
            cat = resource.setdefault(category.name, {})

            for parameter in category.values():
                cat[parameter.name] = parameter.svalue

        self.client[rscpath] = resource
