# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pytils

class School(models.Model):
    name = models.CharField(u"Имя учебного заведения", max_length = 100)

class Grade(models.Model):
    long_name = models.CharField(u"Длинное имя", max_length = 100)
    small_name = models.CharField(u"Короткое имя", max_length = 10)
    school = models.ForeignKey(School, verbose_name = "Школа", blank = True)
    def __unicode__(self):
        return self.long_name

class Subject(models.Model):
    name = models.CharField(u"Предмет", max_length = 100)
    school = models.ForeignKey(School, verbose_name = "Школа", blank = True)
    def __unicode__(self):
        return self.name

class Clerk(User):
    last_name = models.CharField(u"Фамилия", max_length = 30)
    first_name = models.CharField(u"Имя", max_length = 30)
    middle_name = models.CharField(u"Отчество", max_length = 30, blank = True)
    password_journal = models.CharField(u"Пароль доступа к дневнику", max_length = 255)
    school = models.ForeignKey(School, verbose_name = "Школа", blank = True)
    def __unicode__(self):
        result = self.last_name + ' ' + self.first_name + ' ' + self.middle_name
        if self.grade:
            result = result + ' (' + self.grade.small_name + ')'
        return result
    def fio(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name
    def fi(self):
        return self.last_name + ' ' + self.first_name
    def save(self, force_insert=False, force_update=False):
        #Генерация имени пользователя
        username = self.prefix + "."
        last_name = pytils.translit.translify(self.last_name.lower())
        last_name = last_name.replace("'","")
        last_name = last_name.replace("`","")
        first_name = pytils.translit.translify(self.first_name.lower())
        first_name = first_name.replace("'","")
        first_name = first_name.replace("`","")
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
        if self.administrator:
            self.is_                        
        super(Clerk, self).save(force_insert, force_update)
    class Meta:
        abstract = True

class Teacher(Clerk):
    administrator = models.BooleanField(u"Администратор")
    subjects = models.ManyToManyField(Subject, verbose_name = u"Предметы", related_name = 'subjects', blank = True, null = True)
    grades = models.ManyToManyField(Grade, blank = True, verbose_name = u"Классы", related_name = "grades", null = True)
    grade = models.ForeignKey(Grade, verbose_name="Класс", blank = True, related_name = 'grade', null = True)
    current_subject = models.ForeignKey(Subject, blank = True, related_name = 'current_subject', null = True)
    prefix = "t"

class Pupil(Clerk):
    grade = models.ForeignKey(Grade, verbose_name = u"Класс")
    sex = models.CharField(max_length = 1, choices = (('1', u'Юноша'), ('2', u'Девушка')), verbose_name = u'Пол')
    group = models.CharField(max_length = 1, choices = (('1', u'1 группа'), ('2', u'2 группа')), verbose_name = u'Группа')
    special = models.BooleanField(verbose_name = u'Специальная группа')
    prefix = "p"

