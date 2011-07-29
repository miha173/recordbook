#!/usr/bin/python
import sys
import os

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env/lib/python2.6/site-packages'))
sys.path.insert(0, PROJECT_DIR)
activate_this = os.path.dirname(os.path.abspath(__file__)) + '/.env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from odaybook import settings

for app in settings.SOUTH_APPS:
    print app
    os.system('python %s/odaybook/manage.py schemamigration %s --auto' % (PROJECT_DIR, app))
    print ''
