# -*- coding: UTF-8 -*-

import datetime

from django.db import models
from odaybook.userextended.models import Teacher, Subject, Grade
from odaybook.rest.models import RestModel

from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey, SimpleChainedForeignKey

from odaybook.userextended.models import Parent, Pupil

GROUPS = zip(*([str(i) for i in range(1, 11)], )*2)
GROUPS.insert(0, ('0', u'Весь класс'))

class Connection(RestModel):
    teacher = SimpleChainedForeignKey(Teacher, ('subject', 'grade'), ('subjects', 'grades'), verbose_name = u'Учитель')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ForeignKey(Grade, verbose_name = u'Класс')
    connection = models.CharField(verbose_name = u'Связь', max_length = 1, choices = GROUPS, default = '0')
    class Meta:
        ordering = ['teacher']
        unique_together = (('teacher', 'subject', 'grade'), )
        verbose_name = u'Связь'

class Request(models.Model):
    parent = models.ForeignKey(Parent)
    pupil = models.ForeignKey(Pupil)
    activated = models.BooleanField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    activated_timestamp = models.DateTimeField(null = True, blank = True)

    def approve(self):
        self.parent.pupils.add(self.pupil)
        if not self.parent.pupils.all().count():
            self.parent.current_pupil = self.pupil
        self.parent.save()
        self.activated = True
        self.activated_timestamp = datetime.datetime.now()
        # TODO: send mail
        self.save()

    def disapprove(self):
        self.activated = True
        self.activated_timestamp = datetime.datetime.now()
        # TODO: send mail
        self.save()

    
    