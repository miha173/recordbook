# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList

from models import Subject, Teacher, Pupil, Grade, School, Staff, Cam, Option, Achievement, Permission
from src.marks.models import Lesson, ResultDate

class SubjectForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Subject
        fields = ['name']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'prefix', 'saturday', 'url', 'address', 'phone', 'gate_use', 'gate_url', 'gate_id', 'gate_password', 'max_mark', 'gapps_use', 'gapps_login', 'gapps_password', 'gapps_domain', 'private_domain', 'private_salute']
    def __init__(self, school = None, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        self.fields['gapps_password'].widget = forms.PasswordInput()
        self.fields['gate_password'].widget = forms.PasswordInput()
        
class OptionForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Option
        fields = ['key', 'value']

class CamForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(CamForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Cam
        fields = ['name', 'ip', 'device1', 'device1_name', 'device2', 'device2_name']

class GradeForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Grade
        fields = ['number', 'long_name', 'small_name']

class PupilForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(PupilForm, self).__init__(*args, **kwargs)
        self.fields['grade'].queryset = Grade.objects.filter(school = school)
    photo = forms.FileField(required = False)
    class Meta:
        model = Pupil
        fields = ('last_name', 'first_name', 'middle_name', 'sex', 'grade', 'group', 'special', 'cart', 'phone_mother', 'phone_father', 'email')

class StaffForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Staff
        fields = ('last_name', 'first_name', 'middle_name', 'administrator', 'cart')

class TeacherForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['grades'].queryset = Grade.objects.filter(school = school)
        self.fields['subjects'].queryset = Subject.objects.filter(school = school)
        self.fields['grade'].queryset = Grade.objects.filter(school = school)
#        if not Option.objects.filter(key = 'TC_IP', school = school):
#            del self.fields['cart']
    class Meta:
        model = Teacher
        fields = ('last_name', 'first_name', 'middle_name', 'grade', 'grades', 'subjects', 'cart', 'administrator')
    grades = forms.ModelMultipleChoiceField(queryset = Grade.objects.all(), required = False, widget = forms.CheckboxSelectMultiple())
    subjects = forms.ModelMultipleChoiceField(queryset = Subject.objects.all(), required = False, widget = forms.CheckboxSelectMultiple())

class ResultDateForm(forms.ModelForm):
    def __init__(self, school = None, *args, **kwargs):
        super(ResultDateForm, self).__init__(*args, **kwargs)
        self.fields['grades'].widget = forms.CheckboxSelectMultiple()
        self.fields['grades'].queryset = Grade.objects.filter(school = school)
    class Meta:
        model = ResultDate
        fields = ['name', 'period', 'startdate', 'enddate', 'grades']
    startdate = forms.DateField(('%d.%m.%y',), label = u'Дата начала периода', widget=forms.DateTimeInput(format='%d.%m.%y'))
    enddate = forms.DateField(('%d.%m.%y',), label = u'Дата подведения итога', widget=forms.DateTimeInput(format='%d.%m.%y'))

class AchievementForm(forms.ModelForm):
    def __init__(self, pupil = None, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ('%d.%m.%Y', )
        self.fields['date'].widget = forms.DateInput(format = '%d.%m.%Y')
        self.fields['date'].help_text = u'В формате ДД.ММ.ГГГГ'
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'date']

class PermissionForm():
    pass