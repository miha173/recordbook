# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from models import Subject, Teacher, Pupil, Grade, School, Staff, Option, Achievement, Permission, Clerk
from odaybook.marks.models import Lesson, ResultDate

class SubjectForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        self.school = school
        super(SubjectForm, self).__init__(*args, **kwargs)
    def save(self):
        result = super(SubjectForm, self).save(commit = False)
        result.school = self.school
        result.save()
        return result
    class Meta:
        model = Subject
        fields = ['name']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'saturday', 'url', 'address', 'phone',
#                  'prefix', 'gate_use', 'gate_url', 'gate_id', 'gate_password',
                  'max_mark', 'gapps_use', 'gapps_login', 'gapps_password',
                  'gapps_domain', 'private_domain', 'private_salute'
        ]
    def __init__(self, school = None, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        self.fields['gapps_password'].widget = forms.PasswordInput()
        self.fields['url'].initial = 'http://'
#        self.fields['gate_password'].widget = forms.PasswordInput()
        
class OptionForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        self.school = school
        super(OptionForm, self).__init__(*args, **kwargs)
    def save(self):
        result = super(OptionForm, self).save(commit = False)
        result.school = self.school
        result.save()
        return result
    class Meta:
        model = Option
        fields = ['key', 'value']

class GradeForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        self.school = school
        super(GradeForm, self).__init__(*args, **kwargs)
    def save(self):
        result = super(GradeForm, self).save(commit = False)
        result.school = self.school
        result.save()
        return result
    class Meta:
        model = Grade
        fields = ['number', 'long_name', 'small_name']

class ClerkForm(forms.ModelForm):
    class Meta:
        model = Clerk
        fields = [
                'last_name', 'first_name', 'middle_name', 'email', 'phone',
        ]

class PupilForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(PupilForm, self).__init__(*args, **kwargs)
        self.fields['grade'].queryset = Grade.objects.filter(school = school)
    class Meta:
        model = Pupil
        fields = [
                'sex', 'grade', 'group', 'special',
                'parent_phone_1', 'parent_phone_2',
        ]

class StaffForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        if not Option.objects.filter(school = school, key = 'TC_IP'):
            del self.fields['cart']
    class Meta:
        model = Staff
        fields = [
#                'last_name', 'first_name', 'middle_name', 'cart',
                'edu_admin', 'tech_admin',
        ]

class TeacherForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['grades'].queryset = Grade.objects.filter(school = school)
        self.fields['subjects'].queryset = Subject.objects.filter(school = school)
        self.fields['grade'].queryset = Grade.objects.filter(school = school)
        if not Option.objects.filter(school = school, key = 'TC_IP'):
            del self.fields['cart']
    class Meta:
        model = Teacher
        fields = [
#                'last_name', 'first_name', 'middle_name', 'cart', 'administrator'
                'grade', 'grades', 'subjects',
        ]
        
    grades = forms.ModelMultipleChoiceField(queryset = Grade.objects.all(), required = False, widget = forms.CheckboxSelectMultiple())
    subjects = forms.ModelMultipleChoiceField(queryset = Subject.objects.all(), required = False, widget = forms.CheckboxSelectMultiple())
#    def clean_grade(self):
#        if Teacher.objects.filter(school = self.school, grade = self.grade):
#            pass

class AchievementForm(forms.ModelForm):
    def __init__(self, pupil = None, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ('%d.%m.%Y', )
        self.fields['date'].widget = forms.DateInput(format = '%d.%m.%Y')
        self.fields['date'].help_text = u'В формате ДД.ММ.ГГГГ'
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'date']

