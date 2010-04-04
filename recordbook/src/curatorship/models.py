# -*- coding: UTF-8 -*-
from django.db import models
from src.userextended.models import Teacher, Subject, Grade
from src.rest.models import RestModel

class Connection(RestModel):
    teacher = models.ForeignKey(Teacher, verbose_name = u'Учитель')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ForeignKey(Grade, verbose_name = u'Класс')
    connection = models.CharField(verbose_name = u'Связь', max_length = 1, choices = (('0', 'Весь класс'),
                                                                                     ('1', '1 группа'), 
                                                                                     ('2', '2 группа'), 
                                                                                     ('3', 'Юноши'),
                                                                                     ('4', 'Девушки'),
                                                                                     ('5', 'Спец. группа'),
                                                                                     ))