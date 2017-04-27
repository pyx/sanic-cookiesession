from sanic import Sanic, response

import sanic_cookiesession


def test_session():
    app = Sanic('test_app')
    app.config['SESSION_COOKIE_SECRET_KEY'] = "u can't c me"

    sanic_cookiesession.init_app(app)

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

    sanic_cookiesession.init_app(app)

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
