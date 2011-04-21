# -*- coding: UTF-8 -*-
from django.db import models
from odaybook.userextended.models import Teacher, Subject, Grade
from odaybook.rest.models import RestModel

from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey, SimpleChainedForeignKey

from odaybook.userextended.models import Parent, Pupil

class Connection(RestModel):
    teacher = SimpleChainedForeignKey(Teacher, ('subject', 'grade'), ('subjects', 'grades'), verbose_name = u'Учитель')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ForeignKey(Grade, verbose_name = u'Класс')
    connection = models.CharField(verbose_name = u'Связь', max_length = 1, choices = (('0', 'Весь класс'),
                                                                                     ('1', '1 группа'), 
                                                                                     ('2', '2 группа'), 
                                                                                     ('3', 'Юноши'),
                                                                                     ('4', 'Девушки'),
                                                                                     ('5', 'Спец. группа'),
                                                                                     ), 
                                default = '0')
    class Meta:
        ordering = ['teacher']
        unique_together = (('teacher', 'subject', 'grade'), )
        verbose_name = u'Связь'

class Request(models.Model):
    parent = models.ForeignKey(Parent)
    pupil = models.ForeignKey(Pupil)
    activated = models.BooleanField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    activated_timestamp = models.DateTimeField(auto_now_add=True)

    def activate(self):
        pass

    
    