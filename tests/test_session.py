import pytest

from sanic import Sanic, response

import sanic_cookiesession


def test_session():
    app = Sanic('test_app')
    app.config['SESSION_COOKIE_SECRET_KEY'] = "u can't c me"

    sanic_cookiesession.setup(app)

    @app.get('/inc')
    async def inc(request):
        session = request['session']
        value = session['counter'] = session.get('counter', 0) + 1
        return response.text(value)

    @app.get('/dec')
    async def dec(request):
        session = request['session']
        value = session['counter'] = session.get('counter', 0) - 1
        return response.text(value)

    @app.get('/zero')
    async def zero(request):
        value = request['session']['counter'] = 0
        return response.text(value)

    req, resp = app.test_client.get('/zero')
    assert resp.status == 200
    assert resp.text == '0'
    cookies = resp.cookies
    assert cookies

    for i in range(1, 10):
        req, resp = app.test_client.get('/inc', cookies=cookies)
        assert resp.status == 200
        assert resp.text == str(i)
        cookies = resp.cookies
        assert cookies

    req, resp = app.test_client.get('/zero')
    assert resp.status == 200
    assert resp.text == '0'
    cookies = resp.cookies
    assert cookies

    req, resp = app.test_client.get('/dec', cookies=cookies)
    assert resp.status == 200
    assert resp.text == '-1'
    cookies = resp.cookies
    assert cookies

    req, resp = app.test_client.get('/dec', cookies=cookies)
    assert resp.status == 200
    assert resp.text == '-2'
    cookies = resp.cookies
    assert cookies


def test_cookies_tempered():
    app = Sanic('test_app')
    app.config['SESSION_COOKIE_SECRET_KEY'] = "not this time"

    sanic_cookiesession.setup(app)

    @app.get('/')
    async def index(request):
        session = request['session']
        first_time = not session.get('visited')
        if first_time:
            session['visited'] = True
        return response.text('yes' if first_time else 'no')

    req, resp = app.test_client.get('/')
    assert resp.status == 200
    assert resp.text == 'yes'
    cookies = resp.cookies
    assert cookies

    req, resp = app.test_client.get('/', cookies=cookies)
    assert resp.status == 200
    assert resp.text == 'no'
    cookies = resp.cookies
    assert cookies

    req, resp = app.test_client.get('/')
    assert resp.status == 200
    assert resp.text == 'yes'
    cookies = resp.cookies
    assert cookies

    req, resp = app.test_client.get('/', cookies=cookies)
    assert resp.status == 200
    assert resp.text == 'no'
    cookies = resp.cookies
    assert cookies

    cookies['_session'] = 'i am bad'

    req, resp = app.test_client.get('/', cookies=cookies)
    assert resp.status == 200
    assert resp.text == 'yes'
    cookies = resp.cookies
    assert cookies


def test_session_cookie_domain():
    app = Sanic('test_app')
    app.config['SESSION_COOKIE_SECRET_KEY'] = "u can't c me"
    app.config['SESSION_COOKIE_DOMAIN'] = '.example.com'

    sanic_cookiesession.setup(app)

    @app.get('/')
    async def index(request):
        value = request['session']['counter'] = 0
        return response.text(value)

    req, resp = app.test_client.get('/')
    assert resp.status == 200
    assert resp.text == '0'
    cookies = resp.cookies
    assert cookies['_session']['domain'] == '.example.com'


def test_not_overwrite_existing_session():
    app = Sanic('test_app')
    app.config['SESSION_COOKIE_SECRET_KEY'] = "u can't c me"
    # set session name so that this test do not rely on default setting
    app.config['SESSION_NAME'] = 'session'

    this_is_the_session = {}

    # add session object before Sanic-CookieSession
    @app.middleware('request')
    async def add_session(request):
        request['session'] = this_is_the_session

    sanic_cookiesession.setup(app)

    @app.get('/')
    async def index(request):
        assert this_is_the_session is request['session']
        request['session']['name'] = 'penny'
        return response.text('')

    # hit
    req, resp = app.test_client.get('/')
    assert resp.status == 200
    assert resp.text == ''
    assert this_is_the_session['name'] == 'penny'


def test_delete_session_in_request_will_create_new_object():
    app = Sanic('test_app')
    app.config['SESSION_COOKIE_SECRET_KEY'] = "u can't c me"

    hit_count = 0

    class Session(dict):
        def __init__(self, *args, **kwargs):
            nonlocal hit_count
            hit_count += 1
            super().__init__(*args, **kwargs)

    sanic_cookiesession.setup(app, session_type=Session)

    @app.get('/')
    async def index(request):
        # we will only hit this once in this test, so it holds true
        assert hit_count == 1
        # then delete it, response middleware will create a new one to be
        # saved in the cookie-based session storage
        del request['session']
        return response.text('')

    # hit
    req, resp = app.test_client.get('/')
    assert resp.status == 200
    assert resp.text == ''
    assert hit_count == 2


def test_secret_key_required():
    app = Sanic('test_app')
    assert app.config.get('SECRET_KEY') is None
    assert app.config.get('SESSION_COOKIE_SECRET_KEY') is None

    with pytest.raises(RuntimeError):
        # no secret key
        sanic_cookiesession.setup(app)
