# -*- coding: UTF-8 -*-

from django.db import models
from src.userextended.models import Pupil, Teacher, Subject, Grade

class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name = u'Учитель')
    date = models.DateField(u'Дата')
    topic = models.CharField(u'Тема урока', max_length = 200)
    task = models.CharField(u'Домашнее задание', max_length = 200)
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ForeignKey(Grade, verbose_name = u'Класс')

class Mark(models.Model):
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    lesson = models.ForeignKey(Lesson, verbose_name = u'Занятие')
    mark = models.IntegerField(u'Отметка', blank = True)
    absent = models.BooleanField(u'Отсутствовал')
    date = models.DateField(u'Дата выставления', auto_now_add = True)
    comment = models.TextField(u'Комментарий к отметке', blank = True)