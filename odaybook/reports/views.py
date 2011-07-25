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
from odaybook.marks.models import Lesson
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
            # FIXME
            if all == 0:
                rows.append_col(0)
            else:
                rows.append_col((c.count()/all)*100)
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
            # FIXME
            if all == 0:
                rows.append_col(0)
            else:
                rows.append_col((c.count()/all)*100)
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
    rows.append_cols('', u'Заполнено', u'не заполненно больше 10 дней', u'не заполненно больше 15 дней')
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









