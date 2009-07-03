# -*- coding: UTF-8 -*-

from django.db import models
from src.userextended.models import Pupil, Teacher, Subject, Grade, School

class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name = u'Учитель')
    date = models.DateField(u'Дата')
    topic = models.CharField(u'Тема урока', max_length = 200)
    task = models.CharField(u'Домашнее задание', max_length = 200)
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ForeignKey(Grade, verbose_name = u'Класс')
    class Meta:
        ordering = ['-date']

class Mark(models.Model):
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    lesson = models.ForeignKey(Lesson, verbose_name = u'Занятие')
    mark = models.IntegerField(u'Отметка', blank = True, null = True)
    absent = models.BooleanField(u'Отсутствовал')
    date = models.DateField(u'Дата выставления', auto_now_add = True)
    comment = models.TextField(u'Комментарий к отметке', blank = True)
    class Meta:
        ordering = ['-date']

class ResultDate(models.Model):
    school = models.ForeignKey(School)
    period = models.CharField(u'Итоговый период', max_length = 1, choices = (('1', u'1 четверть'),
                                                                       ('2', u'2 четверть'),
                                                                       ('5', u'1 полугодие'),
                                                                       ('3', u'3 четверть'),
                                                                       ('4', u'4 четверть'),
                                                                       ('6', u'2 полугодие'),
                                                                       ))
    date = models.DateField(u'Дата подведения итога')
    grades = models.ManyToManyField(Grade, verbose_name = u'Классы')
    class Meta:
        ordering = ['date']

class Result(models.Model):
    result = models.ForeignKey(ResultDate, verbose_name = u'Период')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    mark = models.IntegerField(u'Отметка')
