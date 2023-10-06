# -*- coding: utf-8 -*-
import logging
from itsdangerous import URLSafeTimedSerializer, BadSignature

__version__ = '0.3.0'

__all__ = ['setup']

log = logging.getLogger(__name__)


def setup(app, session_type=dict, serializer_type=URLSafeTimedSerializer):
    """Setup cookie-based session for :code:`Sanic` application"""
    secret_key = app.config.get('SESSION_COOKIE_SECRET_KEY')
    if not secret_key:
        secret_key = app.config.get('SECRET_KEY')
    if not secret_key:
        raise RuntimeError(
            'either SESSION_COOKIE_SECRET_KEY or SECRET_KEY must be set')

    setdefault = app.config.setdefault
    cookie_name = setdefault('SESSION_COOKIE_NAME', '_session')
    domain = setdefault('SESSION_COOKIE_DOMAIN', None)
    httponly = setdefault('SESSION_COOKIE_HTTPONLY', True)
    max_age = setdefault('SESSION_COOKIE_MAX_AGE', 86400)
    salt = setdefault('SESSION_COOKIE_SALT', 'cookie-session')
    secure = setdefault('SESSION_COOKIE_SECURE', True)
    session_name = setdefault('SESSION_NAME', 'session')

    serializer = serializer_type(secret_key, salt=salt)

    @app.on_request
    async def load_session(request):
        if hasattr(request.ctx, session_name):
            return
        session_cookie = request.cookies.get(cookie_name)
        if session_cookie:
            try:
                session = serializer.loads(session_cookie, max_age=max_age)
            except BadSignature as ex:
                log.warning('%s - %s', ex, ex.payload)
                session = session_type()
        else:
            session = session_type()
        setattr(request.ctx, session_name, session)

    @app.on_response
    async def save_session(request, response):
        session = getattr(request.ctx, session_name, None)
        if session is None:
            setattr(request.ctx, session_name, session := session_type())
        kwargs = {
            "httponly": httponly,
            "max_age": max_age,
            "secure": secure
        }
        if domain:
            kwargs["domain"] = domain

        response.add_cookie(cookie_name, serializer.dumps(session), **kwargs)
