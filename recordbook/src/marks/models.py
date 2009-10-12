# -*- coding: UTF-8 -*-

from django.db import models
from src.userextended.models import Pupil, Teacher, Subject, Grade, School

class LessonManager(models.Manager):
    def search(self, str):
        values = []
        a = super(LessonManager, self).get_query_set().filter(grade__long_name__contains = str)
        for obj in a: values.append(obj.id)
        a = super(LessonManager, self).get_query_set().filter(grade__small_name__contains = str)
        for obj in a: values.append(obj.id)
        a = super(LessonManager, self).get_query_set().filter(topic__contains = str)
        for obj in a: values.append(obj.id)
        return super(LessonManager, self).get_query_set().filter(id__in = values)

class Lesson(models.Model):
    objects = LessonManager()
    teacher = models.ForeignKey(Teacher, verbose_name = u'Учитель')
    date = models.DateField(u'Дата')
    topic = models.CharField(u'Тема урока', max_length = 200)
    task = models.CharField(u'Домашнее задание', max_length = 200, blank = True, null = True)
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ManyToManyField(Grade, verbose_name = u'Класс')
    class Meta:
        ordering = ['-date']
    def delete(self):
        Mark.objects.filter(lesson = self).delete()
        super(Lesson, self).delete()

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
    startdate = models.DateField(verbose_name = u'Дата начала периода')
    enddate = models.DateField(verbose_name = u'Дата подведения итога')
    grades = models.ManyToManyField(Grade, verbose_name = u'Классы')
    class Meta:
        ordering = ['enddate']
    def delete(self):
        Result.objects.filter(result = self).delete()
        super(ResultDate, self).delete()
    def __unicode__(self):
        return self.get_period_display()

class Result(models.Model):
    resultdate = models.ForeignKey(ResultDate, verbose_name = u'Период')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    mark = models.IntegerField(u'Отметка')
