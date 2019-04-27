#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Me'
SITENAME = 'Dango Kajero'
SITEURL = 'http://utcb.ikiu.me'

PATH = 'content'
STATIC_PATHS = ['images','articles','pdfs']
ARTICLE_PATHS = ['articles']
PLUGIN_PATHS = ['plugins']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.nl2br': {},
        'pyembed.markdown':{}
    },
    'output_format': 'html5',
}

FAVICON = '/images/image.ico'
SITELOGO = '/images/image.png'

TIMEZONE = 'Japan'

DEFAULT_LANG = 'ja'
SUMMARY_MAX_LENGTH = 50

DISPLAY_TAGS_INLINE = True
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll aboutはなんかいい感じにやってくれるそう
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

MENUITEMS = (('Archives', '/archives.html'),
        ('Categories', '/categories.html'),
        ('Tags', '/tags.html'),)
LINKS = (('Archives', '/archives.html'),
        ('Categories', '/categories.html'),
        ('Tags', '/tags.html'),)
# Social widget
SOCIAL = (('github', 'https://github.com/dangorogoro'),
        ('twitter', 'https://twitter.com/dango_bot'),)
PLUGINS = ['share_post', 'render_math']
SHARE_POST_INTRO = 'Like this post? Share on:'

DISPLAY_CATEGORIES_ON_MENU = True
DEFAULT_PAGINATION = 10

THEME = './Flex'

USE_FOLDER_AS_CATEGORY = True
# flex config
MAIN_MENU = True
HOME_HIDE_TAGS = True
DISPLAY_PAGES_ON_MENU = True
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
