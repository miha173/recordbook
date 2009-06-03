# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pytils

class Grade(models.Model):
    long_name = models.CharField(u"Длинное имя", max_length = 100)
    small_name = models.CharField(u"Короткое имя", max_length = 10)
    def __unicode__(self):
        return self.long_name

class Subject(models.Model):
    name = models.CharField(u"Предмет", max_length = 100)
    def __unicode__(self):
        return self.name

class Clerk(User):
    last_name = models.CharField(u"Фамилия", max_length = 30)
    first_name = models.CharField(u"Имя", max_length = 30)
    middle_name = models.CharField(u"Отчество", max_length = 30, blank = True)
    password_journal = models.CharField(u"Пароль доступа к дневнику", max_length = 255)
    def __unicode__(self):
        result = self.last_name + ' ' + self.first_name + ' ' + self.middle_name
        if self.grade:
            result = result + ' (' + self.grade.small_name + ')'
        return result
    def save(self, force_insert=False, force_update=False):
        #Генерация имени пользователя
        username = self.prefix + "."
        last_name = pytils.translit.exttranslify(self.last_name.lower())
        first_name = pytils.translit.exttranslify(self.first_name.lower())
        if len(last_name)+len(first_name)>28:
            if len(last_name)>25:
                last_name = last_name[:25]
                first_name = first_name[:3]
            else:
                if len(last_name)>len(first_name):
                    last_name = last_name[:28-len(first_name)]
                else:
                    first_name = first_name[:28-len(first_name)]
        self.username = username + last_name + '.' + first_name
        #Пароль по умолчанию
        self.set_password("1")
        super(Clerk, self).save(force_insert, force_update)
    class Meta:
        abstract = True

class Teacher(Clerk):
    administrator = models.BooleanField(u"Администратор")
    subjects = models.ManyToManyField('userextended.Subject', blank = True, verbose_name = u"Предметы")
    grades = models.ManyToManyField('userextended.Grade', blank = True, verbose_name = u"Классы", related_name = "grades")
    grade = models.ForeignKey('userextended.Grade', verbose_name="Класс", blank = True)
    prefix = "t"

class Pupil(Clerk):
    grade = models.ForeignKey('userextended.Grade', verbose_name="Класс")
    prefix = "p"

class Probe(models.Model):
    pupil = models.ForeignKey('userextended.Pupil')
    subject = models.ForeignKey('userextended.Subject')
    stars = models.IntegerField()