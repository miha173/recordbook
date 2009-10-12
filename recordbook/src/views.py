# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from src.userextended.models import Pupil, Teacher, Subject
from src.curatorship.models import Connection
from src.marks.models import Mark

def render_options(request):
    options = render_objects = options['render_objects'] = {}
    render_objects['page_variants'] = ("страница","страницы","страниц")
    render_objects['pupil_variants'] = ("ученик", "ученика", "учеников")
    pathes = request.path.split('/')
    if pathes.__len__()==3:
        render_objects['path'] = pathes[1]
    if pathes.__len__()>3:
        render_objects['path'] = pathes[2]
    if request.user.username[0] == 't':
        user = Teacher.objects.get(id = request.user.id)
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
        render_objects['subjects'] = subjects
        render_objects['grade'] = user.grade
        render_objects['administrator'] = user.administrator
        render_objects['next'] = request.path
        render_objects['user_type'] = 'teacher'
        render_objects['teacher'] = True
        render_objects['current_subject'] = user.current_subject
    else:
        user = Pupil.objects.get(id = request.user.id)
        render_objects['pupil'] = True
        render_objects['user_type'] = 'pupil'
        marks_list = {}
        render_objects['subjects'] = []
        for connection in Connection.objects.filter(grade = user.grade):
            if connection.connection == '0' or connection.connection == user.group or (int(connection.connection)-2) == user.sex or (int(connection.connection)-4) == int(user.special):
                render_objects['subjects'].append(connection.subject)
    render_objects['user'] = user
    render_objects['school'] = user.school
    return render_objects

@login_required()
def index(request):
    return render_to_response('root/index.html', context_instance=RequestContext(request))