# -*- coding: UTF-8 -*-

from django.db import models
from django.conf import settings

from odaybook.userextended.models import School

class RingTimetable(models.Model):
    u'''
        Заготовка для расписания звонков.
    '''
    number = models.CharField(u"Номер урока", max_length = 1, choices = settings.LESSON_NUMBERS)
    start = models.TimeField(u'Начало урока')
    end = models.TimeField(u'Окончание урока')
    school = models.ForeignKey(School)
    class Meta:
        abstract = True

class UsalRingTimetable(RingTimetable):
    u'''
        Регулярное расписание звонков, повторяющиеся каждую неделю.
    '''
    workday = models.CharField(u"День недели", max_length = 1, choices = settings.WORKDAYS)

class SpecicalRingTimetable(RingTimetable):
    u'''
        Заготовка специального расписания звонков. Нигде не используется
    '''
    date = models.DateField(u"Дата")

class Timetable(models.Model):
    u'''
        Заготовка расписания занятий.
    '''
    from odaybook.userextended.models import Grade, Subject
    grade = models.ForeignKey(Grade)
    number = models.CharField(u"Номер урока", max_length = 2, choices = settings.LESSON_NUMBERS)
    subject = models.ForeignKey(Subject, verbose_name = u"Предмет")
    room = models.CharField(u"Кабинет", max_length = 25, null = True, blank = True)
    group = models.CharField(u"Группа", max_length = 1, choices = ( ('1', '1 группа'), ('2', '2 группа') ))
    school = models.ForeignKey(School)
    class Meta:
        abstract = True
        ordering = ['number']

class UsalTimetable(Timetable):
    u'''
        Регулярное расписание занятий, повторяющиеся каждую неделю.
    '''
    workday = models.CharField(u"День недели", max_length = 1, choices = settings.WORKDAYS)

class SpecicalTimetable(Timetable):
    u'''
        Заготовка специального расписания занятий. Нигде не используется
    '''
    date = models.DateField(u"Дата")

class Holiday(models.Model):
    u'''
        Заготовка каникулярных периодов. Нигде не используется
    '''
    name = models.CharField(u"Имя", max_length = 255)
    start = models.DateField(u"Дата начала")
    end = models.DateField(u"Дата окончания")
    school = models.ForeignKey(School)
