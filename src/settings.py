# -*- coding: UTF-8 -*-

from settings_dist import *

import sys

sys.path.append('/home/entropius/GTD/job/esch/cafeteria')
sys.path.append('/home/entropius/GTD/job/esch/infoFrame')
sys.path.append('/home/entropius/GTD/job/esch/library')
sys.path.append('/home/entropius/GTD/job/ika/guard')

QIWI_LOGIN = '10035'
QIWI_PASSWORD = 'axhrqs7'


INSTALLED_APPS = INSTALLED_APPS + ('django_extensions', 'cafeteria', 'cafeteria.core', 'infoFrame', 'library', 'guard')