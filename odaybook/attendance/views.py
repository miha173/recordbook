# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from odaybook import settings
from odaybook.userextended.models import Grade, Subject, School
from odaybook.userextended.forms import ImportForm
from odaybook.userextended.views import get_grade

from models import UsalTimetable
from utils import TimetableDayPupil, TimetableDayGrade

@login_required
def index(request):
    u'''
        Актуален вопрос необходимости этой страницы. 
    '''
    render = {}
    if request.user.type == 'Parent':
        render['timetables'] = [TimetableDayPupil(workday = workday, pupil = request.user.current_pupil)
                                for workday in request.user.current_pupil.school.get_workdays()]
    return render_to_response('~attendance/page_pupil.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: reduce(lambda x, y: x or y, map(lambda a: a in ['Superuser', 'EduAdmin'], u.types)))
def timetableSelect(request, school = 0):
    u'''
        Выбор класс для заполнения расписания.s
    '''
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
    u'''
        Форма заполнения расписания.

        Внимание: много непонятного
    '''
    render = {}
    if school:
        school = get_object_or_404(School, id = school)
    else:
        school = request.user.school
    render['school'] = school
    render['grade'] = grade = get_object_or_404(Grade, id = id, school = school)

    try:
        current_workday = int(request.GET.get('workday', '1'))
    except ValueError:
        current_workday = 1
    if current_workday not in school.get_workdays():
        current_workday = 1

    render['workdays'] = school.get_workdays_tuple()
    render['current_workday'] = current_workday = school.get_workdays_dict()[current_workday]
    render['lessons'] = settings.LESSON_NUMBERS
    render['subjects'] = grade.get_subjects()
    render['attendance'] = TimetableDayGrade(workday = current_workday[0], grade = grade)

    if request.is_ajax():
        subject = get_object_or_404(Subject, id = request.GET.get('subject'), school = school)
        if request.GET.get('method') == 'add':
            timetable = UsalTimetable(
                    grade = grade,
                    number = request.GET.get('lesson'),
                    subject = subject,
                    group = request.GET.get('group'),
                    school = school,
                    workday = current_workday[0],
                    room = request.GET.get('room', ''),
            )
            timetable.save()
            return HttpResponse(str(timetable.id))
        elif request.GET.get('method') == 'set_room':
            timetable = get_object_or_404(UsalTimetable,
                    id = request.GET.get('lesson_id'),
                    grade = grade,
                    number = request.GET.get('lesson'),
                    subject = subject,
                    group = request.GET.get('group'),
                    school = school,
                    workday = current_workday[0],
            )
            timetable.room = request.GET.get('room', '')
            timetable.save()
        else:
            timetable = get_object_or_404(UsalTimetable,
                    id = request.GET.get('lesson_id'),
                    grade = grade,
                    number = request.GET.get('lesson'),
                    subject = subject,
                    group = request.GET.get('group'),
                    school = school,
                    workday = current_workday[0],
            )
            timetable.delete()
        return HttpResponse('ok')

    return render_to_response('timetableSet.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: reduce(lambda x, y: x or y, map(lambda a: a in ['Superuser', 'EduAdmin'], u.types)))
def importTimetable(request, school):
    '''
        Представление для импорта расписания. Не тестировалась.
    '''
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
                messages.success(request, u'Расписание импортировано')
                return HttpResponseRedirect('..')
    return render_to_response('~attendance/timetableImport.html', render, context_instance = RequestContext(request))
