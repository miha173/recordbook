# -*- coding: UTF-8 -*-

from django import forms
from models import Connection
from src.userextended.models import Pupil, Subject
from src.marks.models import Result, ResultDate

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
    def __init__(self, *args, **kwargs):
        super(ConnectionStep3Wizard, self).__init__(*args, **kwargs)
        self.fields['connection'].initial = '0'

class ConnectionGlobalForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ('teacher', 'subject', 'grade')
    def __init__(self, grade__school, *args, **kwargs):
        return super(ConnectionGlobalForm, self).__init__(*args, **kwargs)
        
class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ('last_name', 'first_name', 'middle_name', 'sex', 'group', 'special')

class GraphiksForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), label = u'Предметы')
    resultDates = forms.ModelMultipleChoiceField(queryset=ResultDate.objects.all(), label = u'Значения')