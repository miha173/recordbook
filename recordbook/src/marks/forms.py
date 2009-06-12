# -*- coding: UTF-8 -*-

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList
from src.marks.models import Lesson, Mark

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ('date', 'topic', 'task', 'grade')
#    def clean_date(self):
#        date = self.cleaned_data['date']
#        try:
#            date = time.strftime('%Y-%m-%d', time.strptime(date, '%d.%m.%Y'))
#        except:
#            self._errros['date'] = u'Дата в неправильном формате. Вводите дату в формате дд.мм.гггг'
#            del self['date']
#        return data

class MarkForm(ModelForm):
    class Meta:
        model = Mark
        fields = ('mark', 'absent', 'comment')
