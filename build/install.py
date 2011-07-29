#!/usr/bin/python
import sys
import os

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, PROJECT_DIR)

activate_this = os.path.dirname(os.path.abspath(__file__)) + '/.env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from odaybook import settings

os.system('%s/build/buildenv.sh' % PROJECT_DIR)

os.system('python %s/odaybook/manage.py syncdb' % PROJECT_DIR)

for app in settings.SOUTH_APPS:
    os.system('python %s/odaybook/manage.py schemamigration %s --initial' % (PROJECT_DIR, app))
    os.system('python %s/odaybook/manage.py migrate %s --fake' % (PROJECT_DIR, app))
