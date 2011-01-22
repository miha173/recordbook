#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

import django.core.handlers.wsgi

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename='/tmp/recordbook.log');

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'
    return _application(environ, start_response)
