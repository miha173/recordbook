# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from models import Teacher, Pupil, Grade, Subject, School
from forms import SubjectForm, GradeForm
from src.views import render_options
from src.curatorship.models import Connection
from src.marks.models import Mark

def index(request):
    return render_to_response('userextended/page.html', render_options(request))

def subjectList(request):
    render = render_options(request)
    paginator = Paginator(Subject.objects.filter(school = Teacher.objects.get(id = request.user.id).school).order_by('name'), 100)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['subjects'] = paginator.page(page)
    except:
        render['subjects'] = paginator.page(paginator.num_pages)
    return render_to_response('userextended/subjectList.html', render)

def subjectEdit(request, mode, subject_id = 0):
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = SubjectForm(instance = get_object_or_404(Subject, id = subject_id))
        elif mode == 'delete':
            Subject.objects.get(id = subject_id).delete()
            return HttpResponseRedirect('/administrator/subject/')
        else:
            render['form'] = SubjectForm()
        return render_to_response('userextended/subject.html', render)
    if request.method == 'POST':
        if mode == 'edit':
            form = SubjectForm(request.POST, instance = get_object_or_404(Subject, id = subject_id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/administrator/subject')
            else:
                render['form'] = form
                return render_to_response('userextended/subject.html', render)
        else:
            form = SubjectForm(request.POST)
            if form.is_valid():
                subject = form.save(commit = False)
                subject.school = Teacher.objects.get(id = request.user.id).school
                subject.save()
                return HttpResponseRedirect('/administrator/subject/')
            else:
                render['form'] = form
                return render_to_response('userextended/subject.html', render)

def gradeList(request):
    render = render_options(request)
    render['grades'] = Grade.objects.filter(school = Teacher.objects.get(id = request.user.id).school).order_by('long_name')
    return render_to_response('userextended/gradeList.html', render)

def gradeEdit(request, mode, grade_id = 0):
    render = render_options(request)
    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = GradeForm(instance = get_object_or_404(Grade, id = grade_id))
        #AHTUNG!
        elif mode == 'delete':
            pass
        else:
            render['form'] = GradeForm()
        return render_to_response('userextended/grade.html', render)
    if request.method == 'POST':
        if mode == 'edit':
            form = GradeForm(request.POST, instance = get_object_or_404(Grade, id = grade_id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/administrator/grade')
            else:
                render['form'] = form
                return render_to_response('userextended/grade.html', render)
        else:
            form = GradeForm(request.POST)
            #AHTUNG!
            if form.is_valid():
                grade = form.save(commit = False)
                grade.school = Teacher.objects.get(id = request.user.id).school
                grade.save()
                return HttpResponseRedirect('/administrator/grade/')
            else:
                render['form'] = form
                return render_to_response('userextended/grade.html', render)
