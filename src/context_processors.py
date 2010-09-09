# -*- coding: UTF-8 -*-

from datetime import date

from django.core.context_processors import request
from django.core.signals import request_started

from src.curatorship.models import Connection
from src.userextended.models import Subject

from src import settings

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
            'DIR': path,}

def environment(request):
    render = {}
    user = request.user
    if request.user.is_authenticated():
        temp = request.user.prefix
        if request.user.prefix == 't':
            render['BASE_TEMPLATE'] = 'page.html'
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
            if settings.ROOT_CAN_ALL:
                if user.is_administrator():
                    render['subjects'] = Subject.objects.filter(school = user.school)
        elif request.user.prefix == 'p':
            render['BASE_TEMPLATE'] = 'page_pupil.html'
            render['subjects'] = user.get_subjects()
        else:
            request.user.is_administrator = lambda: request.user.is_superuser
        if request.user.prefix == 'a' or request.user.is_administrator():
            render['BASE_TEMPLATE'] = 'administrator.html'
    render['ROOT_CAN_ALL'] = settings.ROOT_CAN_ALL
    render['current_year'] = date.today().year
    return render


