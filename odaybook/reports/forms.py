# -*- coding: utf-8 -*-

from django import forms

from odaybook.userextended.models import School

class SchoolSelectForm(forms.Form):
    school = forms.ModelChoiceField(queryset = School.objects.all(), required = True, empty_label = u'Все школы')

