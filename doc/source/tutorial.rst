Tutorial
========

Introduction: Middlewares and URLs
----------------------------------

A *middleware* is a class which can be instantiated with an **URL**.

The middleware is used to provide a Python API for different protocols, those
protocol are used as scheme of the middleware URL to identify which one to
instantiate.

.. code-block:: text

   http://user:pass@localhost:81/path/sub#fragment?foo=bar

The above URL will instantiate the class ``HTTPMiddleware``:

.. code-block:: python

   HTTPMiddleware(
       username='user',
       password='pass',
       hosts=[('localhost', 81)],
       path=['path', 'sub'],
       fragment='fragment',
       foo='bar'
   )

**NB:** As you can see, ``hosts`` is an array, middleware URLs can have multiple
hosts:

.. code-block:: text

   http://user:pass@host1:80,host2:80,host3/path/sub#fragment?foo=bar

With the following instantiation:

.. code-block:: python

   HTTPMiddleware(
       username='user',
       password='pass',
       hosts=[
           ('host1', 80),
           ('host2', 80),
           ('host3', None)
       ],
       path=['path', 'sub'],
       fragment='fragment',
       foo='bar'
   )

Creating a middleware
---------------------

In order to create a middleware for a protocol (database, messaging, ...), you
just need to create a new class inheriting from the ``Middleware`` class, and
register it:

.. code-block:: python

   from link.middleware.core import Middleware, register_middleware


   @register_middleware
   class MyMiddleware(Middleware):
       __protocols__ = ['myprotocol']

       def __init__(self, foo=None, *args, **kwargs):
           super(MyMiddleware, self).__init__(*args, **kwargs)

           self.foo = foo

Then, you can instantiate your new middleware:

.. code-block:: python

   mid = Middleware.get_middleware_by_uri('myprotocol://?foo=bar')
   assert mid.foo == 'bar'
   assert mid.tourl() == 'myprotocol://?foo=bar'

**NB:** In order to be available for the ``Middleware.get_middleware_by_uri()``
method, the middleware **MUST** have been imported first (so the ``register_middleware``
decorator can do its job).

Constraints and child middleware
--------------------------------

Sometimes, your middleware need another middleware to do its job, especially when
your protocol can use multiple backends (i.e.: git via SSH or HTTPS).

Middlewares can have a child middleware specified in the URL:

.. code-block:: text

   git+ssh://user@remotehost/myproject.git

With the following instantiation:

.. code-block:: python

   child = Middleware.get_middleware_by_uri(
       'ssh://user@remotehost/myproject.git'
   )
   mid = MyGitMiddleware(
       username='user',
       hosts=[('remotehost', None)],
       path=['myproject.git']
   )
   mid.set_child_middleware(child)

Then, you can get the child middleware to use it:

.. code-block:: python

   child = mid.set_child_middleware()

Of course, not all middlewares are compatible, you can provide a list of accepted
classes for child middlewares, and the ``set_child_middleware()`` method will check
if the instance match the constraint:

.. code-block:: python

   from link.middleware.core import Middleware, register_middleware


   @register_middleware
   class MyDriver(Middleware):
       __protocols__ = ['mybackend']


   @register_middleware
   class MyMiddleware(Middleware):
       __protocols__ = ['myprotocol']
       __constraints__ = [MyDriver]

And then, someone can inherit from your driver:

.. code-block:: python

   @register_middleware
   class MyCustomDriver(MyDriver):
       _protocols__ = ['mycustombackend']

And instantiate the whole thing:

.. code-block:: python

   mid = Middleware.get_middleware_by_uri(
       'myprotocol+mycustombackend://'
   )

**NB:** There is no limit to how much children you want:

.. code-block:: text

   proto1+proto2+proto3://

Here:

 * ``proto3`` is the child middleware of ``proto2``
 * ``proto2`` is the child middleware of ``proto1``
 * ``proto1`` will be returned by ``Middleware.get_middleware_by_uri()``
