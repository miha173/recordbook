# -*- coding: UTF-8 -*-
from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from src.views import render_options
from src.userextended.models import Teacher, Subject, Grade
from src.curatorship.models import Connection
from src.marks.models import Lesson, Mark
from src.curatorship.forms import ConnectionStep1Wizard, ConnectionStep2Wizard, ConnectionStep3Wizard

def index(request):
    return render_to_response('curatorship/page.html', render_options(request))

def connectionsList(request):
    render = render_options(request)
    teacher = Teacher.objects.get(id = request.user.id)
    render['connections'] = Connection.objects.filter(grade = teacher.grade)
    return render_to_response('curatorship/connectionsList.html', render)

def connectionWizard(request, step):
    render = render_options(request)
    step = int(step)
    if step == 1:
        if request.method == 'GET':
            user = Teacher.objects.get(id = request.user.id)
            render['form'] = ConnectionStep1Wizard()
            render['form'].fields['teacher'].queryset = Teacher.objects.filter(grades = user.grade)
            return render_to_response('curatorship/connectionWizard.html', render)
        else:
            render['form'] = ConnectionStep1Wizard(request.POST)
            if render['form'].is_valid():
                request.session['teacher'] = render['form'].cleaned_data['teacher']
                return HttpResponseRedirect('/curatorship/connections/wizard/2/')
            else:
                user = Teacher.objects.get(id = request.user.id)
                render['form'].fields['teacher'].queryset = Teacher.objects.filter(grades = user.grade)
                return render_to_response('curatorship/connectionWizard.html', render)
    if step == 2:
        if request.method == 'GET':
            render['form'] = ConnectionStep2Wizard()
            render['form'].fields['subject'].queryset = request.session['teacher'].subjects
            return render_to_response('curatorship/connectionWizard.html', render)
        else:
            render['form'] = ConnectionStep2Wizard(request.POST)
            if render['form'].is_valid():
                request.session['subject'] = render['form'].cleaned_data['subject']
                return HttpResponseRedirect('/curatorship/connections/wizard/3')
            else:
                render['form'].fields['subject'].queryset = Subject.objects.filter(teacher = request.session['teacher'])
                return render_to_response('curatorship/connectionWizard.html', render)
    if step == 3:
        if request.method == 'GET':
            render['form'] = ConnectionStep3Wizard()
            return render_to_response('curatorship/connectionWizard.html', render)
        else:
            render['form'] = ConnectionStep3Wizard(request.POST)
            if render['form'].is_valid():
                user = Teacher.objects.get(id = request.user.id)
                connection = Connection(teacher = request.session['teacher'],
                                        subject = request.session['subject'],
                                        grade = user.grade,
                                        connection = render['form'].cleaned_data['connection'])
                connection.save()
                del request.session['teacher']
                del request.session['subject']
                return HttpResponseRedirect('/curatorship/connections/')
            else:
                return render_to_response('curatorship/connectionWizard.html', render)
            
def connectionEdit(request, connection_id, mode):
    if mode == 'delete':
        connection = get_object_or_404(Connection, id = connection_id)
        connection.delete()
        return HttpResponseRedirect('/curatorship/connections/')