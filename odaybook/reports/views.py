# -*- coding: UTF-8 -*-

import demjson
import datetime
import csv
import re

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import get_model
from django.core.urlresolvers import resolve, reverse

from odaybook import settings
from odaybook.userextended.models import Grade, Subject, School, Teacher, Pupil, MembershipChange
from odaybook.attendance.models import UsalTimetable
from odaybook.marks.forms import StatForm
from odaybook.marks.models import Lesson, Mark
from reports import get_fillability
from forms import SchoolSelectForm

class Array(object):

    n = 0 # столбцы
    m = 0 # строки

    def __init__(self):
        super(Array, self).__init__()
        self.current_row = -1
        self.rows = []
        n = m = 0

    def append_col(self, val):
        self.rows[self.current_row].append(unicode(val))
        if self.n < len(self.rows[self.current_row]): self.n += 1

    def append_cols(self, *vals):
        for val in vals:
            self.rows[self.current_row].append(unicode(val))
            if self.n < len(self.rows[self.current_row]): self.n += 1

    def insert_row(self, *rows):
        self.rows.append(list(rows))
        self.current_row += 1
        self.m += 1

    def get_content(self):
        return self.rows[1:]

    def export_to_csv(self):
        result = ''
        for row in self.rows:
            result += ';'.join(['"%s"' % r for r in row]) + '\n'
        return result

    def get_header(self):
        return self.rows[0]

@login_required
@user_passes_test(lambda u: u.type != 'Pupil')
def index(request):
    return render_to_response('~reports/index.html', context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher' and u.edu_admin)
def report_health(request):
    render = {}

    total = {'all': 0}
    rows = Array()
    rows.insert_row()
    rows.append_col('')
    for group in settings.HEALTH_GROUPS:
        rows.append_col(u'%s гр., кол.' % group)
        rows.append_col(u'%s гр., %%' % group)
    rows.append_col(u'Всего')
    for grade in Grade.objects.filter(school = request.user.school):
        rows.insert_row()
        rows.append_col(unicode(grade))
        all = Pupil.objects.filter(grade = grade).count()
        total['all'] += all
        for group in settings.HEALTH_GROUPS:
            c = Pupil.objects.filter(school = request.user.school, grade = grade, health_group = group)
            rows.append_col(c.count())
            total[group] = total.get(group, 0) + c.count()
            if all == 0: rows.append_col(0)
            else: rows.append_col((c.count()/all)*100)
        rows.append_col(str(all))

    rows.insert_row()
    rows.append_col(u'Итого')
    for group in settings.HEALTH_GROUPS:
        rows.append_col(total[group])
        rows.append_col('')
    rows.append_col(total['all'])

    render['rows'] = rows

    if request.GET.get('export_to_csv'):
        response = HttpResponse(rows.export_to_csv(), mimetype = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename=report_health.csv'
        return response

    return render_to_response('~reports/report_health.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Teacher' and u.edu_admin)
def report_order(request):
    render = {}

    total = {'all': 0}
    rows = Array()
    rows.insert_row()
    rows.append_col('')
    for order in settings.PUPIL_ORDER:
        rows.append_col(u'%s., кол.' % order[1])
        rows.append_col(u'%s., %%' % order[1])
    rows.append_col(u'Всего')
    for grade in Grade.objects.filter(school = request.user.school):
        rows.insert_row()
        rows.append_col(unicode(grade))
        all = Pupil.objects.filter(grade = grade).count()
        total['all'] += all
        for order in settings.PUPIL_ORDER:
            c = Pupil.objects.filter(school = request.user.school, grade = grade, order = order[0])
            rows.append_col(c.count())
            total[order[0]] = total.get(order[0], 0) + c.count()
            if all == 0: rows.append_col(0)
            else: rows.append_col((c.count()/all)*100)
        rows.append_col(str(all))

    rows.insert_row()
    rows.append_col(u'Итого')
    for order in settings.PUPIL_ORDER:
        rows.append_col(total[order[0]])
        rows.append_col('')
    rows.append_col(total['all'])

    render['rows'] = rows

    if request.GET.get('export_to_csv'):
        response = HttpResponse(rows.export_to_csv(), mimetype = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename=report_order.csv'
        return response

    return render_to_response('~reports/report_order.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type in ['Superviser', 'Superuser'])
def report_fillability(request):
    render = {}

    total = {}
    rows = Array()
    rows.insert_row()
    rows.append_cols('', u'заполнено, %', u'не заполненно больше 10 дней, % ', u'не заполненно больше 15 дней, %')
    schools = School.objects.all()
    render['form'] = form = SchoolSelectForm(request.GET)
    if form.is_valid():
        schools = schools.filter(id = form.cleaned_data['school'].id)
    all = {
        'filled': 0,
        'not_filled': 0,
        'not_filled_from_10_to_15_days': 0,
        'not_filled_more_15_days': 0,
    }
    for school in schools:
        rows.insert_row()
        fillability = get_fillability(Lesson.objects.filter(grade__school = school))
        for i in fillability:
            if 'percent' not in i and i!='all': all[i] += fillability[i]
        rows.append_col(unicode(school))
        rows.append_cols(
                fillability['filled_percent'],
                fillability['not_filled_from_10_to_15_days_percent'],
                fillability['not_filled_more_15_days_percent'],
        )

    render['rows'] = rows
    render['all'] = all

    if request.GET.get('export_to_csv'):
        response = HttpResponse(rows.export_to_csv(), mimetype = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename=report_order.csv'
        return response

    render['GOOGLE_JS_API'] = True
    
    return render_to_response('~reports/report_fillability.html', render, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.type == 'Superviser')
def report_membershipchanges(request):
    render = {}

    render['form'] = SchoolSelectForm(request.GET)


    objects = MembershipChange.objects.all()

    if render['form'].is_valid():
        objects = objects.filter(school = render['form'].cleaned_data['school'])

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

    return render_to_response('~reports/report_membershipchanges.html', render, context_instance = RequestContext(request))


@login_required
@user_passes_test(lambda u: u.type in ['Superviser', 'Teacher', 'Parent'])
def report_marks(request, mode = 'all'):
    from django import forms
    from odaybook.marks.forms import StatForm

    class PupilSelectForm(forms.Form):
        from smart_selects.form_fields import ChainedModelChoiceField, SimpleChainedModelChoiceField
        school = forms.ModelChoiceField(queryset = School.objects.all(), label = u'Школа', required = False)
        grade = ChainedModelChoiceField(app_name = 'userextended',
                                        model_name = 'Grade',
                                        chain_field = 'school',
                                        model_field = 'school',
                                        queryset = Grade.objects.all(),
                                        label = u'Класс',
                                        required = False
        )
        pupil = ChainedModelChoiceField(app_name = 'userextended',
                                        model_name = 'Pupil',
                                        chain_field = 'grade',
                                        model_field = 'grade',
                                        queryset = Pupil.objects.all(),
                                        label = u'Ученик'
        )
        def __init__(self, school = None, grades = None, grade = None, pupil = None, *args, **kwargs):
            super(PupilSelectForm, self).__init__(*args, **kwargs)
            if school:
                del self.fields['school']
                if grades:
                    self.fields['grade'] = forms.ModelChoiceField(queryset = grades, label = u'Класс')
                else:
                    self.fields['grade'] = forms.ModelChoiceField(queryset = Grade.objects.filter(school = school), label = u'Класс')
            if grade:
                del self.fields['grade']
                self.fields['pupil'] = forms.ModelChoiceField(queryset = Pupil.objects.filter(grade = grade), label = u'Ученик')
            if pupil:
                del self.fields['school']
                del self.fields['grade']
                del self.fields['pupil']
                
    render = {}

    school = grades = grade = pupil = None

    if request.user.type == 'Teacher':
        grades = [g.id for g in request.user.grades.all()]

        if request.user.grade: grades.append(request.user.grade.id)

        if request.user.edu_admin: grades += [g.id for g in Grade.objects.filter(school = request.user.school)]

        school = request.user.school

        grades = set(grades)
        if len(grades) == 0:
            raise Http404()
        elif len(grades) == 1:
            grades = None
            grade = Grade.objects.get(id = grades[0])
        else:
            grades = Grade.objects.filter(id__in = grades)

    elif request.user.type == 'Parent':
        pupil = request.user.current_pupil



    render['pupilSelectForm'] = pupilSelectForm = PupilSelectForm(school = school,
                                                                  grade = grade,
                                                                  grades = grades,
                                                                  pupil = pupil,
                                                                  data = request.GET
                                                                  )

    start = datetime.date.today() - datetime.timedelta(weeks = 2)
    end = datetime.date.today() + datetime.timedelta(days = 1)
    render['form'] = form = StatForm(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
    else:
        render['form'] = StatForm()

    if pupilSelectForm.is_valid() or pupil:
        pupil = render['pupil'] = pupil or pupilSelectForm.cleaned_data['pupil']
        if pupilSelectForm.is_valid():
            render['params'] = {}
            for param in 'school', 'grade', 'pupil':
                render['params'][param] = request.GET.get(param, None)

        if mode == 'all':
            render.update(pupil.get_all_marks(start, end))
        else:
            render.update(pupil.get_result_marks())
    else:
        render['pupilSelectForm'] = PupilSelectForm(school = school,
                                                    grade = grade,
                                                    grades = grades,
                                                    pupil = pupil,
                                                   )

    render['mode'] = mode
    
    return render_to_response('~reports/report_marks.html', render, context_instance = RequestContext(request))



@login_required
def viewMarks(request, id):
    from django.db.models import Avg
    render = {}
    pupil = request.user.current_pupil
    subject = get_object_or_404(Subject, id = id, school = pupil.school)
    subject.teacher = pupil.get_teacher(subject)
    subject.avg = Mark.objects.filter(pupil = pupil, absent = False, lesson__date__gte = datetime.datetime.now() - datetime.timedelta(weeks = 4), lesson__subject = subject).aggregate(Avg('mark'))['mark__avg']
    if subject.avg<3:
        subject.avg_type = "bad"
    elif subject.avg>=4:
        subject.avg_type = "good"
    else:
        subject.avg_type = "normal"
    days = {
        1: u'Пн',
        2: u'Вт',
        3: u'Ср',
        4: u'Чт',
        5: u'Пт',
        6: u'Сб',
    }
    subject.days = []
    lessons = UsalTimetable.objects.filter(grade = pupil.grade,
                                           subject = subject,
                                           group = pupil.groups[subject.id].group).order_by('workday')
    for lesson in lessons:
        if int(lesson.workday) not in subject.days:
            subject.days.append(int(lesson.workday))
    subject.days = [days[day] for day in subject.days]

    start = datetime.date.today() - datetime.timedelta(weeks = 4)
    end = datetime.date.today() + datetime.timedelta(days = 1)
    if request.method == 'GET':
        render['form'] = form = StatForm()
    else:
        render['form'] = form = StatForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
    render['lessons'] = Lesson.objects.filter(grade = pupil.grade, date__gte = start, date__lte = end, subject = subject)
    for lesson in render['lessons']:
        if Mark.objects.filter(pupil = pupil, lesson = lesson):
            lesson.mark = Mark.objects.get(pupil = pupil, lesson = lesson)

    render['subject'] = subject
    return render_to_response('~marks/%s/marks.html' % request.user.type.lower(), render, context_instance = RequestContext(request))





