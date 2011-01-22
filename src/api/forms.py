# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.forms.util import ErrorList
from src.userextended.models import School, Grade, Teacher, Pupil, Subject
from src.marks.models import Lesson, Mark, ResultDate, Result

class SchoolRestForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'saturday']

class GradeRestForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['number', 'long_name', 'small_name', 'school']

class TeacherRestForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'middle_name', 'grade', 'school']


class PupilRestForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'middle_name', 'grade', 'school']


class SubjectRestForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'school']


class LessonRestForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['teacher', 'date', 'topic', 'task', 'subject', 'grade']



class MarkRestForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['pupil', 'lesson', 'mark', 'absent',]

class ResultDateRestForm(forms.ModelForm):
    class Meta:
        model = ResultDate
        fields = ['name', 'school', 'period', 'startdate', 'enddate', 'grades']

class ResultRestForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['resultdate', 'subject', 'pupil', 'mark']

