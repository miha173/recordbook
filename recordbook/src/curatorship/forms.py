# -*- coding: UTF-8 -*-

from django import forms
from src.curatorship.models import Connection


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