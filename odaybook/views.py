# -*- coding: UTF-8 -*-
'''
    Здесь размещаются представления, которые нельзя однозначно отнести
    к какому либо представлению.
'''

from datetime import datetime, timedelta

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.aggregates import Avg


from odaybook.userextended.models import Pupil, Teacher, Notify
from odaybook.curatorship.models import Request
from odaybook.attendance.models import UsalTimetable
from odaybook.attendance.utils import TimetableDayPupil
from odaybook.marks.models import Mark

@login_required()
def index(request):
    '''
        Главная страница. По-хорошему, всё разнести нужно
    '''
    render = {}
    
    if request.user.type == 'Parent':
        pupil = request.user.current_pupil
        render['curator'] = pupil.get_curator().fio()

        render['classmates'] = Pupil.objects.filter(grade = pupil.grade)

        today_timetable = TimetableDayPupil(
                workday = datetime.now().isoweekday(),
                pupil = pupil
        )
        tomorrow_timetable = TimetableDayPupil(
                workday = (datetime.now() + timedelta(days = 1)).isoweekday(),
                pupil = pupil,
                day_date = datetime.now()
        )

        render['timetables'] = [today_timetable,
                                tomorrow_timetable,
                               ]
        
    elif 'Curator' in request.user.types:
        render['requests'] = Request.objects.filter(
                pupil__grade = request.user.grade,
                activated = False
        )
        
    if 'EduAdmin' in request.user.types:
        render['notifies'] = Notify.objects.filter(for_eduadmin = True)

    if request.user.type == 'Superuser':
        render['notifies'] = Notify.objects.filter(for_superviser = True)
        
    return render_to_response(
            'root/index.html',
            render,
            context_instance=RequestContext(request)
    )


@login_required()
@user_passes_test(lambda u: u.type == 'Parent')
def grade(request):
    '''
        Список класса в интерфейсе родителя
    '''
    render = {}
    render['classmates'] = Pupil.objects.filter(
            grade = request.user.current_pupil.grade
    )
    return render_to_response(
            'root/grade_pupil.html',
            render,
            context_instance=RequestContext(request)
    )

@login_required()
@user_passes_test(lambda u: u.type == 'Parent')
def teachers(request):
    '''
        Список учителей в интерфейсе родителя
    '''
    render = {}
    render['teachers'] = request.user.current_pupil.get_teachers()
    return render_to_response(
            'root/teachers.html',
            render,
            context_instance=RequestContext(request)
    )

@login_required()
def teacher(request, id):
    '''
        Информация об учителей в интерфейсе родителя.
        Бессмысленная страница? 
    '''
    render = {}
    render['teacher'] = get_object_or_404(Teacher, id = id)
    return render_to_response(
            'root/teacher.html',
            render,
            context_instance=RequestContext(request)
    )

@login_required()
@user_passes_test(lambda u: u.type == 'Parent')
def subjects(request):
    '''
        Список предметов с информацией в интерфейсе родителя.
    '''
    render = {}
    pupil = request.user.current_pupil
    subject_list = pupil.get_subjects()
    for subject in subject_list:
        subject.teacher = pupil.get_teacher(subject)
        subject.avg = Mark.objects.filter(
                pupil = pupil,
                absent = False,
                lesson__date__gte = datetime.now() - timedelta(weeks = 4),
                lesson__subject = subject
        ).aggregate(Avg('mark'))['mark__avg']
        days = {1: u'Пн',
                2: u'Вт',
                3: u'Ср',
                4: u'Чт',
                5: u'Пт',
                6: u'Вс',
                }
        subject.days = []
        timetable = UsalTimetable.objects.filter(
                grade = pupil.grade,
                subject = subject
        ).order_by('workday')

        for lesson in timetable:
            if int(lesson.workday) not in subject.days:
                subject.days.append(int(lesson.workday))
        subject.days = [days[day] for day in subject.days]
    render['subjects'] = subject_list
    return render_to_response(
            'root/subjects.html',
            render,
            context_instance=RequestContext(request)
    )






