# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from models import Book, Arrearage

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author']


class ArrearageForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author']



