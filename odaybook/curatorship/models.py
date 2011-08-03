# -*- coding: UTF-8 -*-
'''
    Связки учитель<-->класс и заявки на привязку
'''

import datetime

from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string

from smart_selects.db_fields import SimpleChainedForeignKey

from odaybook.userextended.models import Teacher, Subject, Grade
from odaybook.userextended.models import Parent, Pupil
from django.conf import settings

GROUPS = zip(*([str(i) for i in range(1, 11)], )*2)
GROUPS.insert(0, ('0', u'Весь класс'))

class Connection(models.Model):
    '''
        Данная связка позволяет устоновить точное соответветсвие между
        учителем, предметом, классом и группой.

        Это необходимо для случаев, когда преподаватель ведёт уроки только в
        одной группе, или ведёт не все возможные предметы.
    '''
    teacher = SimpleChainedForeignKey(Teacher,
                                      ('subject', 'grade'),
                                      ('subjects', 'grades'),
                                      verbose_name = u'Учитель')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ForeignKey(Grade, verbose_name = u'Класс')
    connection = models.CharField(verbose_name = u'Связь',
                                  max_length = 1,
                                  choices = GROUPS,
                                  default = '0')
    class Meta:
        ordering = ['teacher']
        unique_together = (('teacher', 'subject', 'grade'), )
        verbose_name = u'Связь'

class Request(models.Model):
    '''
        Заявка родителя классному руководителю на привязку ребёнка.
    '''
    parent = models.ForeignKey(Parent)
    pupil = models.ForeignKey(Pupil)
    activated = models.BooleanField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    activated_timestamp = models.DateTimeField(null = True, blank = True)

    def approve(self):
        '''
            Уведомление об одобрении заявки, сохранение.
        '''
        exists = self.parent.pupils.all()
        self.parent.pupils.add(self.pupil)
        if not exists:
            self.parent.current_pupil = self.pupil
        self.parent.save()
        self.activated = True
        self.activated_timestamp = datetime.datetime.now()
        send_mail(u'Система электронных дневников. Одобрение привязки к ученику.',
                  render_to_string('~curatorship/parent_approve_mail.html'),
                  settings['DEFAULT_FROM_EMAIL'], [self.parent.email])
        self.save()

    def disapprove(self):
        '''
            Уведомление об отклонении заявки, сохранение.
        '''
        self.activated = True
        self.activated_timestamp = datetime.datetime.now()
        send_mail(u'Система электронных дневников. Отклонение привязки к ученику.',
                  render_to_string('~curatorship/parent_disapprove_mail.html'),
                  settings['DEFAULT_FROM_EMAIL'], [self.parent.email])
        self.save()

    
    