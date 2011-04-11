#!/usr/bin/python
import sys
import os

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, PROJECT_DIR)

from odaybook import settings

for app in settings.SOUTH_APPS:
    print app
    os.system('python %s/odaybook/manage.py migrate %s' % (PROJECT_DIR, app))
    print ''
