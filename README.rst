===========================================================
Sanic-CookieSession - Simple Cookie-based Session for Sanic
===========================================================

Sanic-CookieSession implements a client side only, cookie-based session to be
used with `Sanic`_.  Similar to the built-in session in Flask.

.. warning::

  The session cookie is signed cryptographically to prevent modification, but
  the content is not encrypted, NEVER store information that need to be kept
  secret.

.. _Sanic: https://github.com/channelcat/sanic


Quick Start
===========


Installation
------------

.. code-block:: sh

  pip install Sanic-CookieSession


How to use it
-------------

.. code-block:: python

  from sanic import Sanic, response
  import sanic_cookiesession

  app = Sanic(__name__)
  app.config['SESSION_COOKIE_SECRET_KEY'] = 'abcd'

  sanic_cookiesession.setup(app)

  @app.route('/')
  def index(request):
      session = request['session']
      session.setdefault('c', 0)
      session['c'] += 1
      return response.text(session['c'])

  if __name__ == '__main__':
      app.run(debug=True)

That's it.

For more details, please see documentation.


License
=======

BSD New, see LICENSE for details.


Links
=====

- `Documentation <http://sanic-cookiesession.readthedocs.org/>`_

- `Issue Tracker <https://github.com/pyx/sanic-cookiesession/issues/>`_

- `Source Package @ PyPI <https://pypi.python.org/pypi/sanic-cookiesession/>`_

- `Mercurial Repository @ bitbucket
  <https://bitbucket.org/pyx/sanic-cookiesession/>`_

- `Git Repository @ Github
  <https://github.com/pyx/sanic-cookiesession/>`_

- `Git Repository @ Gitlab
  <https://gitlab.com/pyx/sanic-cookiesession/>`_

- `Development Version
  <http://github.com/pyx/sanic-cookiesession/zipball/master#egg=sanic-cookiesession-dev>`_
