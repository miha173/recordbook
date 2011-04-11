#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env/lib/python2.6/site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'odaybook.settings'

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'
    return _application(environ, start_response)
