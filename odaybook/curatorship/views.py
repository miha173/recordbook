# -*- coding: UTF-8 -*-
from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from odaybook.userextended.models import Teacher, Subject, Grade, Pupil, School, Parent
from models import Connection
from forms import ConnectionStep1Wizard, ConnectionStep2Wizard, ConnectionStep3Wizard, PupilForm, GraphiksForm, \
                  ParentRequestForm, ParentForm
from odaybook.marks.models import Lesson, Mark, Result

def index(request):
    return render_to_response('~curatorship/index.html', context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def connectionsList(request):
    render = {}
    teacher = Teacher.objects.get(id = request.user.id)
    render['connections'] = Connection.objects.filter(grade = teacher.grade)
    return render_to_response('~curatorship/connectionsList.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def connectionWizard(request, step):
    render = {}
    step = int(step)
    if step == 1:
        if request.method == 'GET':
            render['form'] = ConnectionStep1Wizard()
            render['form'].fields['teacher'].queryset = Teacher.objects.filter(grades = request.user.grade)
            return render_to_response('~curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
        else:
            render['form'] = ConnectionStep1Wizard(request.POST)
            if render['form'].is_valid():
                request.session['teacher'] = render['form'].cleaned_data['teacher']
                if request.session['teacher'].subjects.count()==1:
                    request.session['subject'] = request.session['teacher'].subjects.all()[0]
                    return HttpResponseRedirect('/curatorship/connections/wizard/3/')
                return HttpResponseRedirect('/curatorship/connections/wizard/2/')
            else:
                render['form'].fields['teacher'].queryset = Teacher.objects.filter(grades = request.user.grade)
                return render_to_response('~curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
    if step == 2:
        if request.method == 'GET':
            render['form'] = ConnectionStep2Wizard()
            render['form'].fields['subject'].queryset = request.session['teacher'].subjects
            return render_to_response('~curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
        else:
            render['form'] = ConnectionStep2Wizard(request.POST)
            if render['form'].is_valid():
                request.session['subject'] = render['form'].cleaned_data['subject']
                return HttpResponseRedirect('/curatorship/connections/wizard/3')
            else:
                render['form'].fields['subject'].queryset = Subject.objects.filter(teacher = request.session['teacher'])
                return render_to_response('~curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
    if step == 3:
        if request.method == 'GET':
            render['form'] = ConnectionStep3Wizard()
            return render_to_response('~curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
        else:
            render['form'] = ConnectionStep3Wizard(request.POST)
            if render['form'].is_valid():
                connection = Connection(teacher = request.session['teacher'],
                                        subject = request.session['subject'],
                                        grade = request.user.grade,
                                        connection = render['form'].cleaned_data['connection'])
                connection.save()
                del request.session['teacher']
                del request.session['subject']
                return HttpResponseRedirect('/curatorship/connections/')
            else:
                return render_to_response('~curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
            
@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def connectionEdit(request, connection_id, mode):
    if mode == 'delete':
        connection = get_object_or_404(Connection, id = connection_id)
        teacher = Teacher.objects.get(id = request.user.id)
        if connection.grade == teacher.grade:
            connection.delete()
        return HttpResponseRedirect('/curatorship/connections/')

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def pupilPasswords(request):
    render = {}
    if request.method == 'GET':
        render['pupils'] = Pupil.objects.filter(grade = request.user.grade)
        return render_to_response('~curatorship/pupilPasswordsList.html', render, context_instance = RequestContext(request))
    elif request.method == 'POST':
        pupils = Pupil.objects.filter(grade = request.user.grade)
        render['pupils'] = []
        for pupil in pupils:
            if request.POST.get('pupil-%s' % pupil.id):
                password = User.objects.make_random_password()
                user = User.objects.get(id = pupil.id)
                user.set_password(password)
                user.save()
                render['pupils'].append({'fi': pupil.fi(), 'username': pupil.username, 'password': password})
        return render_to_response('~curatorship/pupilPasswords.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def pupilList(request):
    render = {}
    render['pupils'] = Pupil.objects.filter(grade = request.user.grade)
    return render_to_response('~curatorship/pupilList.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def pupilEdit(request, mode, id = 0):
    render = {}
    if request.method == 'GET':
        if mode == 'edit':
            render['form'] = PupilForm(instance = get_object_or_404(Pupil, id = id))
        elif mode == 'delete':
            try:
                Pupil.objects.get(id = id).delete()
                return HttpResponseRedirect('/curatorship/pupil/')
            except Exception, (error, ):
                return HttpResponseRedirect('/curatorship/pupil/')
        else:
            render['form'] = PupilForm()
        return render_to_response('~curatorship/pupil.html', render, context_instance = RequestContext(request))
    if request.method == 'POST':
        if mode == 'edit':
            form = PupilForm(request.POST, instance = get_object_or_404(Pupil, id = id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/curatorship/pupil/')
            else:
                render['form'] = form
                return render_to_response('~curatorship/pupil.html', render, context_instance = RequestContext(request))
        else:
            form = PupilForm(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.school = request.user.school
                obj.grade = request.user.grade
                obj.save()
                return HttpResponseRedirect('/curatorship/pupil/')
            else:
                render['form'] = form
                return render_to_response('~curatorship/pupil.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def graphiks(request):
    render = {}
    if request.method == 'GET':
        render['form'] = GraphiksForm(school = request.user.school)
    else:
        form = GraphiksForm(school = request.user.school, data = request.POST)
        form.is_valid()
        render['subjects'] = form.cleaned_data['subjects']
        render['resultdates'] = form.cleaned_data['resultDates']
        render['pupils'] = Pupil.objects.filter(grade = request.user.grade)
        for pupil in render['pupils']:
            pupil.dates = []
            for rd in render['resultdates']:
                date = "'" + rd.name + "', "
                for sbj in render['subjects']:
                    if Result.objects.filter(pupil = pupil, subject = sbj, resultdate = rd).count()!=0:
                        date += str(Result.objects.get(pupil = pupil, subject = sbj, resultdate = rd).mark) + ", "
                    else:
                        date += "0, "
                pupil.dates.append(date)
        render['form'] = form
    return render_to_response('~curatorship/graphiks.html', render, context_instance = RequestContext(request))


@login_required()
def send_parent_request(request):
    render = {}

    school = grade = None
    step = 1

    if request.GET.get('school', False):
        render['school'] = school = get_object_or_404(School, id = request.GET.get('school'))
        step = 2
    if request.GET.get('grade', False):
        render['grade'] = grade = get_object_or_404(Grade, id = request.GET.get('grade'))
        step = 3
    if request.GET.get('pupil', False):
        render['pupil'] = pupil = get_object_or_404(Pupil, id = request.GET.get('pupil'), grade = grade)
        step = 4



    if step == 1: render['objects'] = School.objects.all()

    if step == 2:
        render['objects'] = Grade.objects.filter(school = school)

    if step == 3:
        if request.method == 'POST':
            render['form'] = form = ParentRequestForm(grade, data = request.POST)
            if form.is_valid():
                step = 4
                request.user.pupils
                render['pupil'] = pupil = form.pupil
                request.user.pupils.add(pupil)
                request.user.current_pupil = pupil
                request.user.save()
                return HttpResponseRedirect('/')
            else:
                pass
        else:
            render['form'] = ParentRequestForm(grade)

    if step == 4:
        pass

    render['step'] = step

    return render_to_response('~curatorship/send_append_request.html', render, context_instance = RequestContext(request))




        