# -*- coding: UTF-8 -*-

from django.db import models
from src.userextended.models import Pupil, Teacher, Subject

class Lesson(models.Model):
    teacher = models.ForeignKey('userextended.Teacher', verbose_name = u'Учитель')
    date = models.DateField(u'Дата')
    topic = models.CharField(u'Тема урока', max_length = 200)
    task = models.CharField(u'Домашнее задание', max_length = 200)
    subject = models.ForeignKey('userextended.Subject', verbose_name = u'Предмет')
    grades = models.ForeignKey('userextended.Grade', verbose_name = u'Классы')

class Mark(models.Model):
    pupil = models.ForeignKey('userextended.Pupil', verbose_name = u'Ученик')
    lesson = models.ForeignKey('marks.Lesson', verbose_name = u'Занятие')
    mark = models.IntegerField(u'Отметка')
    absent = models.BooleanField(u'Отсутствовал')
    date = models.DateField(u'Дата выставления')
    comment = models.TextField(u'Комментарий к отметке')