#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs'))
activate_this = os.path.dirname(os.path.abspath(__file__)) + '/.env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import django.core.handlers.wsgi

os.environ['DJANGO_SETTINGS_MODULE'] = 'odaybook.settings'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filename='/tmp/odaybook.log');

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'
    return _application(environ, start_response)
