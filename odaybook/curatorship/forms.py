# -*- coding: UTF-8 -*-

from django import forms
from models import Connection
from odaybook.userextended.models import Pupil, Subject
from odaybook.marks.models import Result, ResultDate

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
        fields = ('teacher', 'subject', 'grade', 'connection')
    def __init__(self, grade__school, *args, **kwargs):
        super(ConnectionGlobalForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = self.fields['teacher'].queryset.filter(school = grade__school)
        self.fields['subject'].queryset = self.fields['subject'].queryset.filter(school = grade__school)
        self.fields['grade'].queryset = self.fields['grade'].queryset.filter(school = grade__school)
        
class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = [
#                'last_name', 'first_name', 'middle_name',
                'sex', 'group', 'special',
        ]

class GraphiksForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), label = u'Предметы')
    resultDates = forms.ModelMultipleChoiceField(queryset=ResultDate.objects.all(), label = u'Значения')
    def __init__(self, school, *args, **kwargs):
        super(GraphiksForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.filter(school = school)
        self.fields['resultDates'].queryset = self.fields['resultDates'].queryset.filter(school = school)
