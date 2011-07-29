# -*- coding: UTF-8 -*-
'''
    Большая часть форм реализованы общими средствами Django для работы с HTTP
'''

from datetime import date, timedelta

from django import forms

from models import Lesson

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
