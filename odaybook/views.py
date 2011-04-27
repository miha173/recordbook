# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Avg

from gate import Gate

from odaybook.userextended.models import Pupil, Teacher, Subject, School
from odaybook.userextended.views import objectList
from odaybook.curatorship.models import Connection
from odaybook.attendance.models import UsalTimetable, UsalRingTimetable
from odaybook.attendance.utils import TimetableDay
from odaybook.marks.models import Mark

@login_required
def sms(request):
    render = {}
    gate = Gate(request.user.school.gate_url, request.user.school.gate_id, request.user.school.gate_password)
    render['text'] = gate.getPaymentInfo()['text']
    t = gate.getBalance(request.user.gate_id)
    render['sms'] = t['sms']
    render['account'] = t['account']
    return render_to_response('sms.html', render, context_instance=RequestContext(request))

@login_required()
def index(request):
    render = {}
    if request.user.type == 'Parent':
        pupil = request.user.current_pupil
        render['curator'] = pupil.get_curator().fio()

        render['classmates'] = Pupil.objects.filter(grade = pupil.grade)
        
#        render['timetables'] = [
#                                TimetableDay(grade = pupil.grade, group = pupil.group, workday = datetime.now().isoweekday()),
#                                TimetableDay(grade = pupil.grade, group = pupil.group, workday = (datetime.now() + timedelta(days = 1)).isoweekday()),
#        ]
        
#        render['lessons'] = UsalRingTimetable.objects.filter(workday = datetime.now().isoweekday(), school = request.user.school)
#    elif request.user.type == 'Teacher':
#        return HttpResponseRedirect('/marks/')
    return render_to_response('root/index.html', render, context_instance=RequestContext(request))


@login_required()
def grade(request):
    render = {}
    if request.user.type == 'Parent':
        render['classmates'] = Pupil.objects.filter(grade = request.user.current_pupil.grade)
    return render_to_response('root/grade_pupil.html', render, context_instance=RequestContext(request))

@login_required()
def teachers(request):
    render = {}
    render['teachers'] = request.user.current_pupil.get_teachers()
    return render_to_response('root/teachers.html', render, context_instance=RequestContext(request))

@login_required()
def teacher(request, id):
    render = {}
    render['teacher'] = get_object_or_404(Teacher, id = id)
    return render_to_response('root/teacher.html', render, context_instance=RequestContext(request))

@login_required()
def subjects(request):
    render = {}
    pupil = request.user.current_pupil
    subjects = pupil.get_subjects()
    if pupil.sex == '1': sex = 3 
    else: sex = 4
    for subject in subjects:
#        subject.teacher = Connection.objects.get(Q(connection = 0) | Q(connection = pupil.group) | Q(connection = int(pupil.sex)+2), subject = subject, grade = pupil.grade).teacher
        subject.teacher = Teacher.objects.filter(grades = pupil.grade, subjects = subject)[0]
        subject.avg = Mark.objects.filter(pupil = pupil, absent = False, lesson__date__gte = datetime.now() - timedelta(weeks = 4), lesson__subject = subject).aggregate(Avg('mark'))['mark__avg']
        days = {1: u'Пн',
                2: u'Вт',
                3: u'Ср',
                4: u'Чт',
                5: u'Пт',
                6: u'Вс',
                }
        subject.days = []
        [subject.days.append(int(lesson.workday)) for lesson in UsalTimetable.objects.filter(grade = pupil.grade, subject = subject).order_by('workday') if int(lesson.workday) not in subject.days]
        subject.days = [days[day] for day in subject.days]
    render['subjects'] = subjects
    return render_to_response('root/subjects.html', render, context_instance=RequestContext(request))






