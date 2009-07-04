# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

from models import Teacher, Pupil, Grade, Subject, School
from forms import SubjectForm, GradeForm, PupilForm, TeacherForm, ResultDateForm
from src.views import render_options, is_administrator
from src.curatorship.models import Connection
from src.marks.models import ResultDate

def index(request):
    return render_to_response('userextended/page.html', render_options(request))

@login_required
@user_passes_test(is_administrator)
def objectList4Administrator(request, object):
    return objectList(request, object)

@login_required
@user_passes_test(is_administrator)
def objectEdit4Administrator(request, object, mode, id = 0):
    return objectEdit(request, object, mode, id)

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
    if object == 'resultdate':
        Object = ResultDate
        templ = render['object_name'] = 'resultdate'
    paginator = Paginator(Object.objects.filter(school = Teacher.objects.get(id = request.user.id).school), 40)
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

@login_required
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
    if object == 'resultdate':
        Object = ResultDate
        templ = 'resultdate'
        Form = ResultDateForm
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = Form(instance = get_object_or_404(Object, id = id))
        elif mode == 'delete':
            try:
                Object.objects.get(id = id).delete()
                return HttpResponseRedirect('/administrator/uni/%s' % templ)
            except Exception, (error, ):
                return HttpResponseRedirect(u'/administrator/uni/%s?error=%s' % (templ, error))
        else:
            render['form'] = Form()
        return render_to_response('userextended/%s.html' % templ, render)
    if request.method == 'POST':
        if mode == 'edit':
            form = Form(request.POST, instance = get_object_or_404(Object, id = id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/administrator/uni/%s' % templ)
            else:
                render['form'] = form
                return render_to_response('userextended/%s.html' % templ, render)
        else:
            form = Form(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.school = Teacher.objects.get(id = request.user.id).school
                obj.save()
                return HttpResponseRedirect('/administrator/uni/%s/' % templ)
            else:
                render['form'] = form
                return render_to_response('userextended/%s.html' % templ, render)
