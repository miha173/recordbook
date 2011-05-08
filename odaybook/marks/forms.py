# -*- coding: UTF-8 -*-

from datetime import date, timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from models import Lesson, Mark, Grade, ResultDate
from odaybook.curatorship.models import Connection

from odaybook import settings

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['topic', 'task']
    

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['mark', 'absent', 'comment']
    def clean_mark(self):
        data = self.cleaned_data['mark']
        if data:
            data = int(data)
            if data > 5:
                raise forms.ValidationError(u"Не слишком высокая отметка?")
            elif data < 1:
                raise forms.ValidationError(u"Не слишком низкая отметка?")
            else:
                return data

class ResultForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['mark']
    def clean_mark(self):
        data = self.cleaned_data['mark']
        data = int(data)
        if data > 5:
            raise forms.ValidationError(u"Не слишком высокая отметка?")
        elif data < 1:
            raise forms.ValidationError(u"Не слишком низкая отметка?")
        else:
            return data

class DeliveryForm(forms.Form):
    def __init__(self, school = None, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        if school: self.fields['grades'].queryset = Grade.objects.filter(school = school)
    grades = forms.ModelMultipleChoiceField(queryset = Grade.objects.all(), label = u'Классы', widget = forms.CheckboxSelectMultiple())
    start = forms.DateField(label = u'Дата начала периода')
    end = forms.DateField(label = u'Дата окончания периода')

class StatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StatForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget.format = '%d.%m.%Y'
        self.fields['end'].widget.format = '%d.%m.%Y'
    start = forms.DateField(('%d.%m.%Y','%d.%m.%y'), label = u'Дата начала периода', initial = date.today() - timedelta(weeks = 2))
    end = forms.DateField(('%d.%m.%Y','%d.%m.%y'), label = u'Дата окончания периода', initial = date.today())

def MarkValidator(school):
    def _validator(mark): 
        import re
        if not re.match('^\d+$', mark):
            raise forms.ValidationError(u'Неверная оценка')
        if int(mark) in range(1, max_mark + 1):
            return int(mark)
        else:
            raise forms.ValidationError(u'Неверная оценка')
    max_mark = school.max_mark
    return _validator

class MarksAdminForm(forms.Form):
    def __init__(self, dates, pupil, init, *args, **kwargs):
        super(MarksAdminForm, self).__init__(*args, **kwargs)
        self.pupil = pupil
        for date in dates:
            field = 'mark-%d%d%d' % (date.day, date.month, date.year)
            t = None
            if field in init: t = str(init[field])
            self.fields[field] = forms.CharField(initial = t, validators = [MarkValidator(pupil.school)], required = False, widget = forms.TextInput(attrs = {'size': 1, 'class': 'mark'}))
  

class ResultDateForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(ResultDateForm, self).__init__(*args, **kwargs)
        self.school = school
        self.fields['grades'].widget = forms.CheckboxSelectMultiple()
        self.fields['grades'].queryset = Grade.objects.filter(school = school)
    class Meta:
        model = ResultDate
        fields = ['name', 'period', 'startdate', 'enddate', 'grades']
    def save(self):
        result = super(ResultDateForm, self).save(commit = False)
        result.school = self.school
        result.save()
        return result
    startdate = forms.DateField(('%d.%m.%y',), label = u'Дата начала периода', widget=forms.DateTimeInput(format='%d.%m.%y'))
    enddate = forms.DateField(('%d.%m.%y',), label = u'Дата подведения итога', widget=forms.DateTimeInput(format='%d.%m.%y'))
