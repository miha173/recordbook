# -*- coding: UTF-8 -*-
'''
    Формы из этого модуля могут заимствоваться другими.
'''

from django import forms
from models import Connection
from odaybook.userextended.models import Pupil, Subject, Teacher, Grade

class ConnectionForm(forms.ModelForm):
    '''
        Редактирование связок
    '''
    class Meta:
        model = Connection
        fields = ('teacher', 'subject', 'grade', 'connection')
    def __init__(self, grade__school, grade = None, *args, **kwargs):
        super(ConnectionForm, self).__init__(*args, **kwargs)
        kwargs = {'school': grade__school}
        if grade:
            self.fields['teacher'].queryset = Teacher.objects.filter(grades = grade, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(**kwargs)
        self.fields['grade'].queryset = Grade.objects.filter(**kwargs)
        if grade:
            del self.fields['grade']
        self.grade = grade

    def save(self, *args, **kwargs):
        result = super(ConnectionForm, self).save(commit = False)
        if self.grade:
            result.grade = self.grade
        result.save()
        return result
        
class PupilForm(forms.ModelForm):
    '''
        Редактирование ученика *классным руководителем*
    '''
    class Meta:
        model = Pupil
        fields = [
                'last_name', 'first_name', 'middle_name', 'email', 'phone',
                'sex', 'special', 'order', 'health_group', 'health_note',
                'parent_phone_1', 'parent_phone_2',
        ]

class ParentRequestForm(forms.Form):
    '''
        Форма, которую заполняет родитель, для прикрепления ребёнка.
    '''
    last_name = forms.CharField(label = u'Фамилия', required=True)
    first_name = forms.CharField(label = u'Имя', required=True)
    middle_name = forms.CharField(label = u'Отчество', required=True)

    pupil = None

    def clean(self, *args, **kwargs):
        super(ParentRequestForm, self).clean(*args, **kwargs)
        if not self.errors:
            pupil_get_kwargs = {'grade': self.grade}
            pupil_get_kwargs.update(self.cleaned_data)
            if Pupil.objects.filter(**pupil_get_kwargs).exclude(
                    id__in = [p.id for p in self.parent.pupils.all()]):
                self.pupil = Pupil.objects.get(**pupil_get_kwargs)
            else:
                raise forms.ValidationError(u'Ученик не найден или уже прикреплён к вам')

    def __init__(self, grade, parent = None, *args, **kwargs):
        super(ParentRequestForm, self).__init__(*args, **kwargs)
        self.grade = grade
        self.parent = parent
