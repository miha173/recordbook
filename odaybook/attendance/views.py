# -*- coding: UTF-8 -*-
import re


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

from odaybook import settings
from odaybook.userextended.models import Grade, Subject, School
from odaybook.userextended.forms import ImportForm
from odaybook.userextended.views import get_grade

from models import UsalTimetable, SpecicalTimetable, Holiday, UsalRingTimetable
from utils import TimetableDayPupil

@login_required
def index(request):
    render = {}
    if request.user.type == 'Parent':
        render['timetables'] = [TimetableDayPupil(workday = workday, pupil = request.user.current_pupil) for workday in request.user.current_pupil.school.get_workdays()]
    return render_to_response('~attendance/page_pupil.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: reduce(lambda x, y: x or y, map(lambda a: a in ['Superuser', 'EduAdmin'], u.types)))
#@user_passes_test(lambda u: 'EduAdmin' in u.types)
def timetableSelect(request, school = 0):
    render = {}
    if school:
        school = get_object_or_404(School, id = school)
    else:
        school = request.user.school
    render['school'] = school
    render['grades'] = Grade.objects.filter(school = school)
    return render_to_response('timetableSelect.html', render, context_instance = RequestContext(request))
    
@login_required
@user_passes_test(lambda u: reduce(lambda x, y: x or y, map(lambda a: a in ['Superuser', 'EduAdmin'], u.types)))
def timetableSet(request, id, school = 0):
    from forms import TimetableForm
    from django import forms
    render = {}
    if school:
        school = get_object_or_404(School, id = school)
    else:
        school = request.user.school
    render['school'] = school
    grade = get_object_or_404(Grade, id = id, school = school)
    form = TimetableForm()
    for day in settings.WORKDAYS:
        if not school.saturday and day[0] == 6: continue 
        for lesson in settings.LESSON_NUMBERS:
            for i in xrange(1, 3):
                room = ''
                subject = None
                if UsalTimetable.objects.filter(grade = grade, number = lesson[0], group = i, school = school, workday = day[0]).count() != 0:
                    u = UsalTimetable.objects.get(grade = grade, number = lesson[0], group = i, school = school, workday = day[0])
                    room = u.room
                    subject = u.subject.id
                form.fields['l_r_%s_%s_%d' % (day[0], lesson[0], i)] = forms.CharField(initial = room, required = False)
#                form.fields['l_s_%s_%s_%d' % (day[0], lesson[0], i)] = forms.CharField(initial = room, required = False)
                form.fields['l_s_%s_%s_%d' % (day[0], lesson[0], i)] = forms.ModelChoiceField(initial = subject, queryset = grade.get_subjects_queryset(), required = False)
    if request.method == 'POST':
        form.initial = request.POST
        for day in settings.WORKDAYS:
            if not school.saturday and day[0] == 6: continue 
            for lesson in settings.LESSON_NUMBERS:
                for i in xrange(1, 3):
                    subject = request.POST.get('l_s_%s_%s_%d' % (day[0], lesson[0], i), '')
                    if subject == '': 
                        if UsalTimetable.objects.filter(grade = grade, number = lesson[0], group = i, school = school, workday = day[0]).count() != 0:
                            UsalTimetable.objects.filter(grade = grade, number = lesson[0], group = i, school = school, workday = day[0]).delete()
                        continue
                    subject = get_object_or_404(Subject, id = subject, school = school)
                    if UsalTimetable.objects.filter(grade = grade, number = lesson[0], group = i, school = school, workday = day[0]).count() == 0:
                        tt = UsalTimetable(grade = grade, number = lesson[0], group = i, school = school, workday = day[0])
                    else:
                        tt = UsalTimetable.objects.get(grade = grade, number = lesson[0], group = i, school = school, workday = day[0])
                    tt.subject = subject
                    tt.room = request.POST.get('l_r_%s_%s_%d' % (day[0], lesson[0], i), '')
                    tt.save()
    render['form'] = form
    return render_to_response('timetableSet.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_administrator())
def ringtimetableList(request, school):
    from forms import RingTimetableForm
    from django import forms
    render = {}
    if school:
        school = get_object_or_404(School, id = school)
    else:
        school = request.user.school
    render['school'] = school
    form = RingTimetableForm()
    for day in settings.WORKDAYS:
        if not school.saturday and day[0] == 6: continue 
        for lesson in settings.LESSON_NUMBERS:
            if UsalRingTimetable.objects.filter(number = lesson[0], school = school, workday = day[0]).count() != 0:
                u = UsalRingTimetable.objects.get(number = lesson[0], school = school, workday = day[0])
                start = u.start
                end = u.end
            else:
                start = end = None
            form.fields['l_s_%s_%s' % (day[0], lesson[0])] = forms.TimeField(initial = start)
            form.fields['l_e_%s_%s' % (day[0], lesson[0])] = forms.TimeField(initial = end)
    if request.method == 'POST':
        form.initial = request.POST
        for day in settings.WORKDAYS:
            if not school.saturday and day[0] == 6: continue 
            for lesson in settings.LESSON_NUMBERS:
                start = request.POST.get('l_s_%s_%s' % (day[0], lesson[0]), '').replace('-', ':')
                if start == '': 
                    if UsalRingTimetable.objects.filter(number = lesson[0], school = school, workday = day[0]).count() != 0:
                        UsalRingTimetable.objects.filter(number = lesson[0], school = school, workday = day[0]).delete()
                    continue
                if UsalRingTimetable.objects.filter(number = lesson[0], school = school, workday = day[0]).count() == 0:
                    tt = UsalRingTimetable(number = lesson[0], school = school, workday = day[0])
                else:
                    tt = UsalRingTimetable.objects.get(number = lesson[0], school = school, workday = day[0])
                tt.start = start
                tt.end = request.POST.get('l_e_%s_%s' % (day[0], lesson[0]), '').replace('-', ':')
                if not (re.match('^\d2:\d2$', tt.start) and re.match('^\d2:\d2$', tt.end)) : continue
                tt.save()
    render['form'] = form
    return render_to_response('ringtimetable.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: reduce(lambda x, y: x or y, map(lambda a: a in ['Superuser', 'EduAdmin'], u.types)))
def importTimetable(request, school):
    # not tested
    import csv
    render = {}
    if request.user.type == 'EduAdmin':
        if request.user.school.id != int(school): raise Http404
    render['school'] = school = get_object_or_404(School, id = school)

    if request.method == 'GET':
        render['form'] = form = ImportForm()
    else:
        render['form'] = form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            workday = 0
            last_grade = None
            render['errors'] = errors = []
            objects = []
            rows = csv.reader(form.cleaned_data['file'], delimiter = ';')
            i = 0
            for row in rows:
                i += 1
                if len(row)<4:
                    errors.append({'line': i, 'column': 0, 'error': u'неверное количество столбцов'})
                    continue
                try:
                    row = ";".join(row)
                    row = row.decode('cp1251')
                except:
                    errors.append({'line': i, 'column': 0, 'error': u'некорректное значение (невозможно определить кодировку)'})
                    continue
                row = row.split(';')
                if last_grade != row[0]:
                   workday = 0
                if int(row[1]) == 1: workday += 1

                number = int(row[1])

                last_grade = grade = row[0]
                try:
                    grade = Grade.objects.get(school = school, **get_grade(grade))
                except Grade.DoesNotExist:
                    errors.append({'line': i, 'column': 0, 'error': u'неизвестный класс %s' % grade})
                    continue

                row[2] = row[2].strip()
                _subjects = row[2].split(',')
                subjects = []
                for sbj in _subjects:
                    try:
                        subjects.append(Subject.objects.get(school = school, name = sbj.strip()))
                    except Subject.DoesNotExist:
                        errors.append({'line': i, 'column': 2, 'error': u'неизвестный предмет %s' % sbj})

                rooms = row[3].split(',')

                ut_kwargs = {'school': school, 'grade': grade, 'workday': workday, 'number': number}
                if len(subjects) == 1 and len(rooms)==1:
                   for j in xrange(1, 3): objects.append(UsalTimetable(subject = subjects[0], room = rooms[0], group = j, **ut_kwargs))

                elif len(subjects) == 1 and len(rooms)==2:
                   for j in xrange(1, 3): objects.append(UsalTimetable(subject = subjects[0], room = rooms[j-1], group = j, **ut_kwargs))

                elif (len(subjects) == 2 and len(rooms)==2) or (len(subjects) == 2 and len(rooms)==3):
                   for j in xrange(1, 3): objects.append(UsalTimetable(subject = subjects[j-1], room = rooms[j-1], group = j, **ut_kwargs))

                elif len(subjects) == 1 and len(rooms)==3:
                   for j in xrange(1, 4): objects.append(UsalTimetable(subject = subjects[0], room = rooms[j-1], group = j, **ut_kwargs))

                else:
                   errors.append({'line': i, 'column': 0, 'error': u'неверный формат строки'})

            if len(errors) == 0:
                for obj in objects:
                    obj.save()
                # FIXME: message
                return HttpResponseRedirect('..')
    return render_to_response('~attendance/timetableImport.html', render, context_instance = RequestContext(request))
