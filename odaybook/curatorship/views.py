# -*- coding: UTF-8 -*-
'''
Инструментарий для облегчения жизни классному руководителю
'''

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test

from odaybook.userextended.models import Teacher, Grade, Pupil, School
from odaybook.userextended.forms import PupilConnectionForm
from models import Connection, Request
from forms import PupilForm, ParentRequestForm

def index(request):
    '''
        Главная страница раздела. Нужно заполнить содержанием.
    '''
    return render_to_response(
            '~curatorship/index.html',
            context_instance=RequestContext(request)
    )

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def connectionsList(request):
    '''
    Список связок.
    '''
    render = {}
    teacher = Teacher.objects.get(id = request.user.id)
    render['connections'] = Connection.objects.filter(grade = teacher.grade)
    return render_to_response(
            '~curatorship/connectionsList.html',
            render,
            context_instance=RequestContext(request)
    )

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def connectionEdit(request, connection_id, mode):
    '''
        Связки пока можно только удалять.
    '''
    if mode == 'delete':
        connection = get_object_or_404(Connection, id = connection_id)
        teacher = Teacher.objects.get(id = request.user.id)
        if connection.grade == teacher.grade:
            connection.delete()
        return HttpResponseRedirect('/curatorship/connections/')

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def pupilList(request):
    '''
        Работа с учениками
    '''
    render = {}
    render['pupils'] = Pupil.objects.filter(grade = request.user.grade)
    return render_to_response('~curatorship/pupilList.html',
                              render,
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def pupilEdit(request, mode, id = 0):
    '''
        Работа с учениками
    '''
    render = {}
    if request.method == 'GET':
        if mode == 'edit':
            pupil = get_object_or_404(Pupil, id = id)
            render['groups'] = [PupilConnectionForm(sbj, pupil, prefix = sbj.id)
                                for sbj in pupil.grade.get_subjects()
                                if sbj.groups]
            render['form'] = PupilForm(instance = pupil)
        elif mode == 'delete':
            try:
                Pupil.objects.get(id = id).delete()
                return HttpResponseRedirect('/curatorship/pupil/')
            except Exception:
                return HttpResponseRedirect('/curatorship/pupil/')
        else:
            render['form'] = PupilForm()
            render['groups'] = [PupilConnectionForm(sbj, prefix = sbj.id)
                                for sbj in request.user.grade.get_subjects()
                                if sbj.groups]

    if request.method == 'POST':
        if mode == 'edit':
            pupil = get_object_or_404(Pupil, id = id)
            form = PupilForm(request.POST, instance = pupil)
            render['groups'] = [PupilConnectionForm(sbj, pupil, data = request.POST, prefix = sbj.id)
                                for sbj in pupil.grade.get_subjects()
                                if sbj.groups]
            form_factory_valid = all([f.is_valid() for f in render['groups']])
            if form.is_valid() and form_factory_valid:
                form.save()
                for f in render['groups']:
                    f.save()
                return HttpResponseRedirect('/curatorship/pupil/')
            else:
                render['form'] = form
        else:
            form = PupilForm(request.POST)
            render['groups'] = [PupilConnectionForm(sbj, data = request.POST, prefix = sbj.id)
                                for sbj in request.user.grade.get_subjects()
                                if sbj.groups]
            form_factory_valid = all([f.is_valid() for f in render['groups']])
            if form.is_valid() and form_factory_valid:
                obj = form.save(commit = False)
                obj.school = request.user.school
                obj.grade = request.user.grade
                obj.save()
                for f in render['groups']:
                    f.save(pupil = obj)
                return HttpResponseRedirect('/curatorship/pupil/')
            else:
                render['form'] = form
    return render_to_response(
            '~curatorship/pupil.html',
            render,
            context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.type == 'Parent')
def send_parent_request(request):
    '''
        Отправка запроса родителем на прикрепление ребёнка. 
    '''
    render = {}

    school = grade = None
    step = 1

    for param in ['school', 'grade']:
        try:
            int(request.GET.get(param, False))
        except:
            raise Http404

    if request.GET.get('school', False):
        render['school'] = school = get_object_or_404(School, id = request.GET.get('school'))
        step = 2
    if request.GET.get('grade', False):
        render['grade'] = grade = get_object_or_404(Grade, id = request.GET.get('grade'))
        step = 3

    if step == 1:
        render['objects'] = School.objects.all()

    if step == 2:
        render['objects'] = Grade.objects.filter(school = school)

    if step == 3:
        if request.method == 'POST':
            render['form'] = form = ParentRequestForm(grade, parent = request.user, data = request.POST)
            if form.is_valid():
                step = 4
                Request(parent = request.user, pupil = form.pupil).save()
            else:
                pass
        else:
            render['form'] = ParentRequestForm(grade)

    render['step'] = step

    return render_to_response(
            '~curatorship/send_append_request.html',
            render,
            context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def requests(request, mode):
    '''
        Одобрение и отклонение заявки на прикрепление
    '''
    request = get_object_or_404(Request,
                                id = request.GET.get('id', 0),
                                pupil__grade = request.user.grade,
                                activated = False)
    if mode == 'approve':
        request.approve()
    else:
        request.disapprove()
    return HttpResponse('')



        