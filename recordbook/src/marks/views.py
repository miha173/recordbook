# -*- coding: UTF-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from src.userextended.models import Pupil, Teacher, Subject, Grade
from src.marks.forms import LessonForm

def render_options(request):
    if request.user.username[:1] == 't':
        user = Teacher.objects.get(id = request.user.id)
        subjects = []
        for subject in user.subjects.all():
            subjects.append({'id': subject.id, 'name': subject.name})
        try:
            user.current_subject
        except ObjectDoesNotExist:
            if subjects.__len__()==1:
                user.current_subject = Subject.objects.get(id = subjects[0]['id'])
        options = {}
        render_objects = {}
        render_objects['user'] = user
        render_objects['subjects'] = subjects
        render_objects['next'] = request.path
        options['render_objects'] = render_objects
        options['usertype'] = 'teacher'
        return options
    else:
        pass

@login_required
def index(request):
    render_res = render_options(request)
    return render_to_response('marks/%s/index.html' % render_res['usertype'], render_res['render_objects'])

def set_current_subject(request, subject_id):
    teacher = Teacher.objects.get(id = request.user.id)
    teacher.current_subject = Subject.objects.get(id = subject_id)
    teacher.save()
    return HttpResponseRedirect(request.GET['next'])

def lesson(request):
    pass
