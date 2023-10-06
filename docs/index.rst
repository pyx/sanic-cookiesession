.. include:: ../README.rst


Configuration
=============

================================= =============================================
Option                            Description
================================= =============================================
:code:`SESSION_COOKIE_DOMAIN`     Set the domain of cookie. Default to
                                  :code:`None`
:code:`SESSION_COOKIE_HTTPONLY`   Set the :code:`HttpOnly` flag of the session
                                  cookie. Default to :code:`True`
:code:`SESSION_COOKIE_MAX_AGE`    How long the session cookie should be valid,
                                  in seconds.  Default is :code:`86400`,
                                  roughly one day.
:code:`SESSION_COOKIE_NAME`       The name of cookie that stores the session.
                                  Default is :code:`_session`
:code:`SESSION_COOKIE_SALT`       The salt used in addition to the secret key
                                  to sign the session cookie. Can be used as
                                  namespace. Default to :code:`cookie-session`
:code:`SESSION_COOKIE_SECRET_KEY` The secret key used to sign the session
                                  cookie, if this is not set,
                                  :code:`SECRET_KEY` will be used instead.
:code:`SESSION_COOKIE_SECURE`     Set the :code:`Secure` flag of the session
                                  cookie. Default to :code:`True`.
:code:`SESSION_NAME`              The name of session object in request.
                                  Default is :code:`session`
================================= =============================================


API
===

.. automodule:: sanic_cookiesession
  :members:


Full Example
============

.. literalinclude:: ../examples/counter.py


Changelog
=========

- 0.3.1

  New release for latest Sanic (currently 23.6)

- 0.2.0

  API changed: changed setup function's name

- 0.1.0

  First public release.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
