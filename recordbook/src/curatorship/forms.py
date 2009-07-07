# -*- coding: UTF-8 -*-

from django import forms
from models import Connection
from src.userextended.models import Pupil

class ConnectionStep1Wizard(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ('teacher',)

class ConnectionStep2Wizard(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ('subject',)

class ConnectionStep3Wizard(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ('connection',)
        
class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ('last_name', 'first_name', 'middle_name', 'sex', 'group', 'special')
