# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from models import Teacher, Pupil, Grade, Subject, School
from forms import SubjectForm, GradeForm, PupilForm, TeacherForm
from src.views import render_options
from src.curatorship.models import Connection
from src.marks.models import Mark

def index(request):
    return render_to_response('userextended/page.html', render_options(request))

def objectList(request, object):
    render = render_options(request)
    if object == 'grade':
        Object = Grade
        templ = render['object_name'] = 'grade'
    if object == 'subject':
        Object = Subject
        templ = render['object_name'] = 'subject'
    if object == 'pupil':
        Object = Pupil
        templ = render['object_name'] = 'pupil'
    if object == 'teacher':
        Object = Teacher
        templ = render['object_name'] = 'teacher'
    paginator = Paginator(Object.objects.filter(school = Teacher.objects.get(id = request.user.id).school), 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)
    render['paginator'] = paginator.num_pages - 1
    return render_to_response('userextended/%sList.html' % templ, render)

def objectEdit(request, object, mode, id = 0):
    if object == 'grade':
        Object = Grade
        templ = 'grade'
        Form = GradeForm
    if object == 'subject':
        Object = Subject
        templ = 'subject'
        Form = SubjectForm
    if object == 'pupil':
        Object = Pupil
        templ = 'pupil'
        Form = PupilForm
    if object == 'teacher':
        Object = Teacher
        templ = 'teacher'
        Form = TeacherForm
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = Form(instance = get_object_or_404(Object, id = id))
        elif mode == 'delete':
            try:
                Object.objects.get(id = id).delete()
                return HttpResponseRedirect('/administrator/%s' % templ)
            except Exception, (error, ):
                return HttpResponseRedirect(u'/administrator/%s?error=%s' % (templ, error))
        else:
            render['form'] = Form()
        return render_to_response('userextended/%s.html' % templ, render)
    if request.method == 'POST':
        if mode == 'edit':
            form = Form(request.POST, instance = get_object_or_404(Object, id = id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/administrator/%s' % templ)
            else:
                render['form'] = form
                return render_to_response('userextended/%s.html' % templ, render)
        else:
            form = Form(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.school = Teacher.objects.get(id = request.user.id).school
                obj.save()
                return HttpResponseRedirect('/administrator/%s/' % templ)
            else:
                render['form'] = form
                return render_to_response('userextended/%s.html' % templ, render)
