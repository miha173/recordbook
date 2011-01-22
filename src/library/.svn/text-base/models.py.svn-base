# -*- coding: utf-8 -*-
from django.db import models

from src.userextended.models import Pupil, School

class Book(models.Model):
    school = models.ForeignKey(School)
    name = models.CharField(verbose_name = u'Название', max_length = 255)
    author = models.CharField(verbose_name = u'Автор', max_length = 255)
    
class Arrearage(models.Model):
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    book = models.ForeignKey(Book, verbose_name = u'Книга')
    take = models.DateField(u'Дата выдачи', auto_now_add = True)
    owe_back = models.DateField(u'Вернуть до')
    back = models.DateField(u'Вернул', auto_now_add = True)
    repeat = models.IntegerField(default = 0)

