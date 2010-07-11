# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from models import Test, Question, VariantA, VariantB

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'subject', 'grades', 'mark5', 'mark4', 'mark3', 'public', 'share']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name']

class VariantAForm(forms.ModelForm):
    class Meta:
        model = VariantA
        fields = ['task', 'answer', 'option1', 'option2', 'option3', 'option4']

class VariantBForm(forms.ModelForm):
    class Meta:
        model = VariantB
        fields = ['task', 'answer']
