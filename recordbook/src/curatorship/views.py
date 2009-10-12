# -*- coding: UTF-8 -*-
from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from src.userextended.models import Teacher, Subject, Grade, Pupil
from models import Connection
from forms import ConnectionStep1Wizard, ConnectionStep2Wizard, ConnectionStep3Wizard, PupilForm
from src.marks.models import Lesson, Mark

def index(request):
    return render_to_response('curatorship/page.html', context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def connectionsList(request):
    render = {}
    teacher = Teacher.objects.get(id = request.user.id)
    render['connections'] = Connection.objects.filter(grade = teacher.grade)
    return render_to_response('curatorship/connectionsList.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def connectionWizard(request, step):
    render = {}
    step = int(step)
    if step == 1:
        if request.method == 'GET':
            render['form'] = ConnectionStep1Wizard()
            render['form'].fields['teacher'].queryset = Teacher.objects.filter(grades = request.user.grade)
            return render_to_response('curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
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
                return render_to_response('curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
    if step == 2:
        if request.method == 'GET':
            render['form'] = ConnectionStep2Wizard()
            render['form'].fields['subject'].queryset = request.session['teacher'].subjects
            return render_to_response('curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
        else:
            render['form'] = ConnectionStep2Wizard(request.POST)
            if render['form'].is_valid():
                request.session['subject'] = render['form'].cleaned_data['subject']
                return HttpResponseRedirect('/curatorship/connections/wizard/3')
            else:
                render['form'].fields['subject'].queryset = Subject.objects.filter(teacher = request.session['teacher'])
                return render_to_response('curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
    if step == 3:
        if request.method == 'GET':
            render['form'] = ConnectionStep3Wizard()
            return render_to_response('curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
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
                return render_to_response('curatorship/connectionWizard.html', render, context_instance = RequestContext(request))
            
@login_required
@user_passes_test(lambda u: u.prefix=='t')
def connectionEdit(request, connection_id, mode):
    if mode == 'delete':
        connection = get_object_or_404(Connection, id = connection_id)
        teacher = Teacher.objects.get(id = request.user.id)
        if connection.grade == teacher.grade:
            connection.delete()
        return HttpResponseRedirect('/curatorship/connections/')

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def pupilPasswords(request):
    render = {}
    if request.method == 'GET':
        render['pupils'] = Pupil.objects.filter(grade = request.user.grade)
        return render_to_response('curatorship/pupilPasswordsList.html', render, context_instance = RequestContext(request))
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
        return render_to_response('curatorship/pupilPasswords.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
def pupilList(request):
    render = {}
    render['pupils'] = Pupil.objects.filter(grade = request.user.grade)
    return render_to_response('curatorship/pupilList.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.prefix=='t')
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
        return render_to_response('curatorship/pupil.html', render, context_instance = RequestContext(request))
    if request.method == 'POST':
        if mode == 'edit':
            form = PupilForm(request.POST, instance = get_object_or_404(Pupil, id = id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/curatorship/pupil/')
            else:
                render['form'] = form
                return render_to_response('curatorship/pupil.html', render, context_instance = RequestContext(request))
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
                return render_to_response('curatorship/pupil.html', render, context_instance = RequestContext(request))
