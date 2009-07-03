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
        fields = ('date', 'topic', 'task', 'grade')
    date = forms.DateField(('%d.%m.%Y',), label=u'Дата', widget=forms.DateTimeInput(format='%d.%m.%Y'))

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('mark', 'absent', 'comment')

class ResultForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('mark')

