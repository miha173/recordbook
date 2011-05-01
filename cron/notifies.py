#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'libs'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'odaybook.settings'

from odaybook.userextended.models import Teacher, Notify
from odaybook.marks.models import Mark
from odaybook.curatorship.models import Request

for teacher in Teacher.objects.all():
    try:
        mark = Mark.objects.filter(lesson__teacher = teacher).latest('date')
        notify_start = mark.date
    except Mark.DoesNotExist:
        mark = Mark(date = datetime.datetime.now() - datetime.timedelta(weeks = 48))
        notify_start = None
    if (datetime.datetime.now() - mark.date).days < 10: continue
    try: notify = Notify.objects.get(user = teacher, type = '1')
    except Notify.DoesNotExist: notify = Notify(user = teacher, type = '1')
    notify.notify_start = notify_start
    if (datetime.datetime.now() - mark.date).days == 15: notify.for_superviser = True
    notify.save()

for teacher in Teacher.objects.filter(last_login__lte = datetime.datetime.now() - datetime.timedelta(days = 5)):
    try: notify = Notify.objects.get(user = teacher, type = '2')
    except Notify.DoesNotExist: notify = Notify(user = teacher, type = '2')
    if (datetime.datetime.now() - teacher.last_login).days >= 10: notify.for_superviser = True
    notify.notify_start = teacher.last_login
    notify.save()

for request in Request.objects.filter(created_timestamp = datetime.datetime.now() - datetime.timedelta(days = 7), activated = False):
    teacher = Teacher.objects.get(grade = request.pupil.grade)
    try: notify = Notify.objects.get(user = teacher, type = '3')
    except Notify.DoesNotExist: notify = Notify(user = teacher, type = '3')
    if (datetime.datetime.now() - teacher.last_login).days >= 15: notify.for_superviser = True
    notify.notify_start = request.created_timestamp
    notify.save()
