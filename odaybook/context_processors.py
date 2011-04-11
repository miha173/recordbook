# -*- coding: UTF-8 -*-

from datetime import date

from django.core.context_processors import request
from django.core.signals import request_started

from odaybook.curatorship.models import Connection
from odaybook.userextended.models import Subject

from odaybook import settings

def plural(request):
    plural = {}
    plural['page_plural'] = (u"страница", u"страницы", u"страниц")
    plural['pupil_plural'] = ("ученик", "ученика", "учеников")
    return plural

def menu(request):
    dirs = request.path.split('/')
    url = dirs[1]
    if len(dirs) == 1:
        url = ''
    path = ''
    if len(dirs)>3:
        path = dirs[2]
    if path == 'uni':
        path = dirs[3]
    return {'ACTIVE_URL': url,
            'DIR': path,
            'path': path,
            }

def environment(request):
    render = {}
    user = request.user
    if request.user.is_authenticated():
        if request.user.type == 'Teacher':
            user = user.current_role.c
            subjects = []
            last_subject = None
            for connection in Connection.objects.filter(teacher = user).order_by('subject'):
                if last_subject != connection.subject:
                    last_subject = connection.subject
                    subjects.append({'id': connection.subject.id, 'name': connection.subject.name})
            if not user.current_subject:
                if len(subjects) != 0:
                    user.current_subject = Subject.objects.get(id = subjects[0]['id'])
                    user.save()
            render['subjects'] = subjects
        elif request.user.type == 'Pupil':
            render['subjects'] = user.get_subjects()
    render['current_year'] = date.today().year
    return render


