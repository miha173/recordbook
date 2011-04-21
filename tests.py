# -*- coding: utf-8 -*-

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'odaybook.settings'
sys.path.insert(0, '/home/entropius/GTD/job/recordbook/sochi/libs')

from odaybook.userextended.models import Pupil, Teacher, Clerk

clerk_id = 1

#clerk = Clerk(last_name = u'Комков', first_name = u'Саша', email = 'sashakomkov@gmail.com')
#clerk.save()grou
#print clerk.id

clerk = Clerk.objects.get(id = clerk_id)

pupil = Pupil(sex = '1')
pupil.set_clerk(clerk)
pupil.save()
pupil.set_roles(clerk)
pupil.save()
print pupil

