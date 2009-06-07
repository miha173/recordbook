# -*- coding: UTF-8 -*-

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList
from src.marks.models import Lesson

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ('date', 'topic', 'task', 'grade')