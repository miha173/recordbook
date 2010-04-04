# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Avg

from src.userextended.models import Pupil, Teacher, Subject, School
from src.userextended.views import objectList4Administrator
from src.curatorship.models import Connection
from src.attendance.models import UsalTimetable
from src.attendance.utils import TimetableDay
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
    render = {}
    if request.user.prefix == 'p':
        pupil = request.user
        render['curator'] = pupil.curator().fio()
        
        render['classmates'] = Pupil.objects.filter(grade = pupil.grade)
        
        render['timetable'] = TimetableDay(grade = pupil.grade, group = pupil.group, workday = datetime.now().isoweekday())
    if request.user.prefix == 'a':
        return objectList4Administrator(request, 'school')
    return render_to_response('root/index.html', render, context_instance=RequestContext(request))


@login_required()
def grade(request):
    render = {}
    if request.user.prefix == 'p':
        render['classmates'] = Pupil.objects.filter(grade = request.user.grade)
    return render_to_response('root/grade_pupil.html', render, context_instance=RequestContext(request))

@login_required()
def teachers(request):
    render = {}
    render['teachers'] = request.user.get_teachers()
    return render_to_response('root/teachers.html', render, context_instance=RequestContext(request))

@login_required()
def teacher(request, id):
    render = {}
    render['teacher'] = get_object_or_404(Teacher, id = id)
    return render_to_response('root/teacher.html', render, context_instance=RequestContext(request))

@login_required()
def subjects(request):
    render = {}
    pupil = request.user
    subjects = request.user.get_subjects()
    if pupil.sex == '1': sex = 3 
    else: sex = 4
    for subject in subjects:
        subject.teacher = Connection.objects.get(Q(connection = 0) | Q(connection = pupil.group) | Q(connection = int(pupil.sex)+2), subject = subject, grade = pupil.grade).teacher
        subject.avg = Mark.objects.filter(pupil = pupil, absent = False, date__gte = datetime.now() - timedelta(weeks = 4), lesson__subject = subject).aggregate(Avg('mark'))['mark__avg']
        days = {1: u'Пн',
                2: u'Вт',
                3: u'Ср',
                4: u'Чт',
                5: u'Пт',
                6: u'Вс',
                }
        subject.days = []
        [subject.days.append(int(lesson.workday)) for lesson in UsalTimetable.objects.filter(grade = pupil.grade, subject = subject, group = pupil.group).order_by('workday') if int(lesson.workday) not in subject.days]
        subject.days = [days[day] for day in subject.days]
    render['subjects'] = subjects
    return render_to_response('root/subjects.html', render, context_instance=RequestContext(request))






