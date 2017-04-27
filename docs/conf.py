#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Sanic-CookieSession documentation build configuration file, created by
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, PROJECT_DIR)
import sanic_cookiesession  # noqa

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'

master_doc = 'index'

project = 'Sanic-CookieSession'
copyright = '2017, Philip Xu'
author = 'Philip Xu and contributors'

release = sanic_cookiesession.__version__
version = release.rsplit('.', 1)[0]

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'alabaster'

html_theme_options = {
    'github_banner': True,
    'github_repo': 'sanic-cookiesession',
    'github_user': 'pyx',
}

htmlhelp_basename = 'Sanic-CookieSessiondoc'


latex_documents = [
    (master_doc, 'Sanic-CookieSession.tex', 'Sanic-CookieSession Documentation',
     'Philip Xu and contributors', 'manual'),
]

man_pages = [
    (master_doc, 'sanic-cookiesession', 'Sanic-CookieSession Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'Sanic-CookieSession', 'Sanic-CookieSession Documentation',
     author, 'Sanic-CookieSession', 'One line description of project.',
     'Miscellaneous'),
]
