# -*- coding: UTF-8 -*-
'''
    Большая часть форм реализованы общими средствами Django для работы с HTTP
'''

from datetime import date, timedelta

from django import forms

from models import Lesson
from odaybook.marks.models import ResultDate
from odaybook.userextended.models import Grade

class LessonForm(forms.ModelForm):
    '''
        Работа с уроком. Не факт, что используется.
    '''
    class Meta:
        model = Lesson
        fields = ['topic', 'task']

class StatForm(forms.Form):
    '''
        Универсальная форма для выбора диапазона дат статистики.
        Используется в различных приложениях.
    '''
    def __init__(self, *args, **kwargs):
        super(StatForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget.format = '%d.%m.%Y'
        self.fields['end'].widget.format = '%d.%m.%Y'
    start = forms.DateField(('%d.%m.%Y','%d.%m.%y'),
                            label = u'Дата начала периода',
                            initial = date.today() - timedelta(weeks = 2))
    end = forms.DateField(('%d.%m.%Y','%d.%m.%y'),
                          label = u'Дата окончания периода',
                          initial = date.today())


class ResultDateForm(forms.ModelForm):
    '''
        Форма для создания итоговых оценок.
    '''
    def __init__(self, school = None, *args, **kwargs):
        super(ResultDateForm, self).__init__(*args, **kwargs)
        self.school = school
        self.fields['grades'].widget = forms.CheckboxSelectMultiple()
        self.fields['grades'].help_text = ''
        self.fields['grades'].queryset = Grade.objects.filter(school = school)
        self.fields['date'].widget.format = '%d.%m.%Y'
        if not school:
            del self.fields['grades']
    class Meta:
        model = ResultDate
        fields = ['name', 'date', 'grades']
    def save(self):
        result = super(ResultDateForm, self).save(commit = False)
        result.school = self.school
        result.save()
        self.save_m2m()
        return result
    date = forms.DateField(('%d.%m.%y','%d.%m.%Y',), label = u'Дата подведения итога')
