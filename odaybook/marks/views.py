# -*- coding: UTF-8 -*-
from datetime import date, timedelta

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages

from odaybook.userextended.models import Pupil, Subject, Grade
from odaybook.curatorship.models import Connection
from odaybook.attendance.models import UsalTimetable

from models import Lesson, Mark, ResultDate
from forms import LessonForm, StatForm

@login_required
def index(request):
    '''
        Очень обширная страница, необходимо сделать разделение. 
    '''
    render = {}
    if request.user.type == 'Parent':
        start = date.today() - timedelta(weeks = 2)
        end = date.today() + timedelta(days = 1)
        if request.method == 'GET':
            render['form'] = form = StatForm()
        else:
            render['form'] = form = StatForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start']
                end = form.cleaned_data['end']

        render.update(request.user.current_pupil.get_all_marks(start, end))

    elif request.user.type == 'Teacher':
        import demjson

        if request.GET.get('set_current_grade', False):
            grade = get_object_or_404(Grade,
                                      id = request.GET.get('set_current_grade'))
            if grade not in request.user.grades.all():
                raise Http404(u'Нет такого класса')
            request.user.current_grade = grade
            request.user.save()
        
        render['lesson_form'] = LessonForm()
        if request.GET.get('set_lesson', False):
            lesson = get_object_or_404(Lesson,
                                       id = int(request.GET.get('lesson', 0)),
                                       teacher = request.user)
            form = LessonForm(request.GET, instance = lesson)
            if form.is_valid():
                form.save()
            return HttpResponse('ok')
        
        if request.GET.get('get_lesson_info', False):
            lesson = get_object_or_404(Lesson,
                                       id = int(request.GET.get('lesson', 0)),
                                       teacher = request.user)
            return HttpResponse(demjson.encode({'task': lesson.task or '',
                                                'topic': lesson.topic or ''}))
            
        
        if request.GET.get('set_mark', False):
            from templatetags.marks_chart import get_mark
            pupil = get_object_or_404(Pupil,
                                      id = int(request.GET.get('pupil', 0)),
                                      grade = request.user.current_grade)
            lesson = get_object_or_404(Lesson,
                                       id = int(request.GET.get('lesson', 0)),
                                       teacher = request.user)
            mark = unicode(request.GET.get('mark', 0)).lower()
            Mark.objects.filter(pupil = pupil, lesson = lesson).delete()
            m = Mark(pupil = pupil, lesson = lesson)
            tr_id = 'p-%d-%d' % (pupil.id, lesson.id)
            if mark not in ['1', '2', '3', '4', '5', 'n', u'н', '']:
                return HttpResponse(demjson.encode({'id': tr_id, 'mark': 'no'}))
            if mark == '':
                return HttpResponse(demjson.encode({'id': tr_id, 'mark': ''}))
            if mark in [u'n', u'н']:
                m.absent = True
            else:
                m.mark = int(mark)
            m.save()
            return HttpResponse(demjson.encode({'id': tr_id,
                                                'mark': get_mark(pupil, lesson),
                                                'mark_value': str(m).strip(),
                                                'mark_type': m.get_type()
                                                }, encoding = 'utf-8'))
        
        from pytils import dt
        if not request.user.current_grade:
            if request.user.get_grades():
                request.user.current_grade = request.user.get_grades()[0]
                request.user.save()
            else:
                messages.error(request, u'К вам не привязано классов')
                return HttpResponseRedirect('/')
        request.user.current_grade.get_pupils_for_teacher_and_subject(
                request.user, request.user.current_subject
        )
        
        try:
            day, month, year = request.GET.get('date', '').split('.')
            date_start = date(day = day, month = month, year = year)
        except ValueError:
            date_start = date.today()

        lessons_range = []
        render['monthes'] = monthes = {}
        for i in xrange(1, 13):
            monthes[i] = ('', 0)
        
        kwargs = {
            'subject': request.user.current_subject,
            'grade': request.user.current_grade
        }
        conn = Connection.objects.filter(teacher = request.user, **kwargs)
        if not conn:
            raise Http404('No connections')
        conn = conn[0]
        if conn.connection != '0':
            kwargs['group'] = conn.connection

        kwargs4lesson = {}
        for i in xrange(14, -1, -1):
            d = date_start - timedelta(days = i)
            kwargs['workday'] = str(d.weekday()+1)
            if UsalTimetable.objects.filter(**kwargs):
                kwargs4lesson = {'teacher': request.user,
                                 'date': d,
                                 'subject': request.user.current_subject}
                groups = {}
                for lesson in UsalTimetable.objects.filter(**kwargs):
                    groups[lesson.group] = groups.get(lesson.group, 0) + 1
                groups = groups.values()
                if Lesson.objects.filter(grade = request.user.current_grade, **kwargs4lesson).count() != max(groups):
                    for j in xrange(max(groups) - Lesson.objects.filter(**kwargs4lesson).count()):
                        t = Lesson(**kwargs4lesson)
                        t.save()
                        t.grade.add(request.user.current_grade)
                        t.save()
            resultdates = ResultDate.objects.filter(date = d, grades = request.user.current_grade)
            if resultdates:
                resultdate = resultdates[0]
                kwargs4lesson = {
                    'resultdate': resultdate,
                    'grade': request.user.current_grade,
                    'subject': request.user.current_subject,
                    'teacher': request.user
                }
                if not Lesson.objects.filter(**kwargs4lesson):
                    del kwargs4lesson['grade']
                    lesson = Lesson(topic = resultdate.name,
                                    date = resultdate.date,
                                    **kwargs4lesson)
                    lesson.save()
                    lesson.grade.add(request.user.current_grade)
                    lesson.save()

        if len(kwargs4lesson) == 0:
            raise Http404(u'Нет расписания')

        del kwargs4lesson['date']
        kwargs4lesson['date__gte'] = date_start - timedelta(days = 15)
        for lesson in Lesson.objects.filter(**kwargs4lesson).order_by('date'):
            monthes[lesson.date.month] = (dt.ru_strftime(u'%B', lesson.date),
                                          monthes[lesson.date.month][1] + 1)
            lessons_range.append(lesson)

        for i in monthes.keys():
            if monthes[i][1] == 0:
                del monthes[i]
        render['lessons'] = lessons_range
        
    return render_to_response(
            '~marks/%s/index.html' % request.user.type.lower(),
            render,
            context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher')
def set_current_subject(request, subject_id):
    '''
        Установка текущего предмета учителя для работы с журналом.
    '''
    request.user.current_subject = Subject.objects.get(id = subject_id)
    request.user.save()
    next_url = request.GET.get('next', '/marks/').strip()
    return HttpResponseRedirect(next_url)

@login_required
def marksView(request, subject_id):
    '''
        Просмотр оценок по данному предмету. Для родительского интерфейса
    '''
    render = {}
    objects = Mark.objects.filter(
            pupil = request.user.current_pupil,
            lesson__subject = get_object_or_404(Subject, id=subject_id)
    ).order_by('-lesson__date')

    paginator = Paginator(objects, settings.PAGINATOR_OBJECTS)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        render['objects'] = paginator.page(page)
    except:
        render['objects'] = paginator.page(paginator.num_pages)

    render['paginator'] = paginator.num_pages - 1
    request.user.current_subject = int(subject_id)
    return render_to_response('~marks/pupil/marks.html',
                              render,
                              context_instance=RequestContext(request))






