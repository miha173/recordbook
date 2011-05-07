# -*- coding: utf-8 -*-

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'odaybook.settings'
sys.path.insert(0, '/home/entropius/GTD/job/recordbook/sochi/libs')

from odaybook.userextended.models import Pupil, Teacher, Clerk, Superuser

clerk_id = 1

#clerk = Clerk(last_name = u'Комков', first_name = u'Саша', email = 'sashakomkov@gmail.com')
#clerk.save()grou
#print clerk.id

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filename='/tmp/recordbook.log');

user = Superuser.objects.get(id = 1)

user.clerk.set_password('12')
user.clerk.save()

