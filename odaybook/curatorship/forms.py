# -*- coding: UTF-8 -*-

from django import forms
from models import Connection
from odaybook.userextended.models import Pupil, Subject, Parent
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

class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ('teacher', 'subject', 'grade', 'connection')
    def __init__(self, grade__school, *args, **kwargs):
        super(ConnectionForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = self.fields['teacher'].queryset.filter(school = grade__school)
        self.fields['subject'].queryset = self.fields['subject'].queryset.filter(school = grade__school)
        self.fields['grade'].queryset = self.fields['grade'].queryset.filter(school = grade__school)
        
class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = [
                'last_name', 'first_name', 'middle_name', 'email', 'phone',
                'sex', 'grade', 'special', 'order', 'health_group', 'health_note',
                'parent_phone_1', 'parent_phone_2',
        ]

class GraphiksForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), label = u'Предметы')
    resultDates = forms.ModelMultipleChoiceField(queryset=ResultDate.objects.all(), label = u'Значения')
    def __init__(self, school, *args, **kwargs):
        super(GraphiksForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.filter(school = school)
        self.fields['resultDates'].queryset = self.fields['resultDates'].queryset.filter(school = school)

class ParentRequestForm(forms.Form):
    last_name = forms.CharField(label = u'Фамилия', required=True)
    first_name = forms.CharField(label = u'Имя', required=True)
    middle_name = forms.CharField(label = u'Отчество', required=True)

    def clean(self, *args, **kwargs):
        super(ParentRequestForm, self).clean(*args, **kwargs)
        if not self.errors:
            pupil_get_kwargs = {'grade': self.grade}
            pupil_get_kwargs.update(self.cleaned_data)
            if Pupil.objects.filter(**pupil_get_kwargs):
                self.pupil = Pupil.objects.get(**pupil_get_kwargs)
            else:
                raise forms.ValidationError(u'Ученик не найден')

    def __init__(self, grade, *args, **kwargs):
        super(ParentRequestForm, self).__init__(*args, **kwargs)
        self.grade = grade

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['last_name', 'first_name', 'middle_name', 'email']

    def __init__(self, pupil, *args, **kwargs):
        self.pupil = pupil
        super(Parent, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        result = super(Parent, self).save(*args, **kwargs)
        result.pupils.add(self.pupil)
        result.save()
        return result
