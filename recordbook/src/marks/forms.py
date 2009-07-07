# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from models import Lesson, Mark
from src.curatorship.models import Connection

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['date', 'topic', 'task', 'grade']
    date = forms.DateField(('%d.%m.%y',), label=u'Дата', widget=forms.DateTimeInput(format='%d.%m.%y'))

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['mark', 'absent', 'comment']
    def clean_mark(self):
        data = self.cleaned_data['mark']
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

