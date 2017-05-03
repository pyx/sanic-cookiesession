# -*- coding: utf-8 -*-
from sanic import Sanic, response

import sanic_cookiesession


app = Sanic('test_app')
app.config['SESSION_COOKIE_SECRET_KEY'] = "u can't c me"
app.config['SESSION_COOKIE_SECURE'] = False

sanic_cookiesession.setup(app)


def render(session):
    tpl = """<a href="/inc">+</a> {} <a href="/dec">-</a>"""
    return response.html(tpl.format(session['counter']))


@app.get('/')
async def index(request):
    return render(request['session'])


@app.get('/inc')
async def inc(request):
    request['session']['counter'] += 1
    return response.redirect('/')


@app.get('/dec')
async def dec(request):
    request['session']['counter'] -= 1
    return response.redirect('/')


@app.middleware('request')
async def create_counter(request):
    request['session'].setdefault('counter', 0)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
