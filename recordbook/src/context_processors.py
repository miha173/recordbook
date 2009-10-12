# -*- coding: UTF-8 -*-

from django.core.context_processors import request
from django.core.signals import request_started

from src.curatorship.models import Connection
from src.userextended.models import Subject

from src import settings

def plural(request):
    plural = {}
    plural['page_plural'] = ("страница","страницы","страниц")
    plural['pupil_plural'] = ("ученик", "ученика", "учеников")
    return plural

def menu(request):
    dirs = request.path.split('/')
    url = dirs[1]
    path = ''
    if len(dirs)>3:
        path = dirs[2]
    if path == 'uni':
        path = dirs[3]
    return {'ACTIVE_URL': url,
            'DIR': path,}

def environment(request):
    render = {}
    user = request.user
    if request.user.is_authenticated():
        if request.user.username[0] == 't':
            subjects = []
            last_subject = None
            for connection in Connection.objects.filter(teacher = user).order_by('subject'):
                if last_subject != connection.subject:
                    last_subject = connection.subject
                    subjects.append({'id': connection.subject.id, 'name': connection.subject.name})
            if not user.current_subject:
                if subjects.__len__() != 0:
                    user.current_subject = Subject.objects.get(id = subjects[0]['id'])
                    user.save()
            render['subjects'] = subjects
        else:
            render['subjects'] = [connection.subject for connection in Connection.objects.filter(grade = user.grade) if connection.connection == '0' or connection.connection == user.group or (int(connection.connection)-2) == user.sex or (int(connection.connection)-4) == int(user.special)]
    return render


