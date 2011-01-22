# -*- coding: utf-8 -*-

import decimal

from django.db import models

from src.userextended.models import Pupil, Teacher, Staff

class Transaction(models.Model):
    user_id = models.IntegerField()
    user_type = models.CharField(max_length = 1, choices = (('p', 'p'), ('t', 't'), ('s', 's')))
    date = models.DateTimeField(verbose_name = u'дата', auto_now_add = True)
    sum = models.DecimalField(verbose_name = u'Сумма', max_digits = 20, decimal_places = 2)
    comment = models.TextField(verbose_name = u'Комментарий')
    def save(self, *args, **kwargs):
        user = self.user()
        user.account -= self.sum
        user.save()
        super(Transaction, self).save(*args, **kwargs)
    def user(self):
        if self.user_type == 'p': Model = Pupil
        elif self.user_type == 't': Model = Teacher
        elif self.user_type == 's': Model = Staff
        return Model.objects.get(id = self.user_id)
        
