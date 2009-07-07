# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pytils


class School(models.Model):
    u'Модель для школ'
    name = models.CharField(u"Имя учебного заведения", max_length = 100)
    prefix = models.CharField(u"Префикс для пароля", max_length = 5)
    def __unicode__(self):
        return self.name

class Grade(models.Model):
    u'Классы в школах'
    long_name = models.CharField(u"Длинное имя", max_length = 100)
    small_name = models.CharField(u"Короткое имя", max_length = 10, blank = True)
    school = models.ForeignKey(School, verbose_name = "Школа")
    def __unicode__(self):
        return self.long_name
    def delete(self):
        if Pupil.objects.filter(grade = self).count() == 0:
            from src.marks.models import Mark, Lesson
            lessons =  Lesson.objects.filter(grade = self)
            Mark.objects.filter(lesson__in = lessons).delete()
            lessons.delete()
            for teacher in Teacher.objects.filter(grade = self):
                teacher.grade = None
                teacher.save()
            for teacher in Teacher.objects.filter(grades = self):
                teacher.grades.remove(self)
                teacher.save()
            super(Grade, self).delete()
        else:
            raise Exception(u"В классе числятся ученики")
    class Meta:
        ordering = ['long_name']

class Subject(models.Model):
    u'Учебные дисциплины'
    name = models.CharField(u"Наименование", max_length = 100)
    school = models.ForeignKey(School, verbose_name = "Школа")
    def __unicode__(self):
        return self.name
    def delete(self):
        from src.curatorship.models import Connection
        from src.marks.models import Mark, Lesson
        Connection.objects.filter(subject = self).delete()
        lessons = Lesson.objects.filter(subject = self)
        if lessons.count()<>0:
            Mark.objects.filter(lesson = lessons).delete()
            lessons.delete()
        if Teacher.objects.filter(subjects = self).count()!=0:
            teacher.subjects.remove(self)
        super(Subject, self).delete()
    class Meta:
        ordering = ['name']

class Clerk(User):
    u'Базовый класс расширенного пользователя. Потомки - учителя, ученики.'
    last_name = models.CharField(u"Фамилия", max_length = 30)
    first_name = models.CharField(u"Имя", max_length = 30)
    middle_name = models.CharField(u"Отчество", max_length = 30, blank = True)
    password_journal = models.CharField(u"Пароль доступа к дневнику", max_length = 255)
    school = models.ForeignKey(School, verbose_name = "Школа")
    def __unicode__(self):
        result = self.last_name + ' ' + self.first_name + ' ' + self.middle_name
        if self.grade:
            result = result + ' (' + self.grade.small_name + ')'
        return result
    def fio(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name
    #Не всегда нужны полные ФИО
    def fi(self):
        return self.last_name + ' ' + self.first_name
    def gen_username(self, school = False):
        #Генерация имени пользователя
        username = self.prefix + "."
        #Удаление нехороших символов из траслитерации
        last_name = pytils.translit.translify(self.last_name.lower())
        last_name = last_name.replace("'","")
        last_name = last_name.replace("`","")
        first_name = pytils.translit.translify(self.first_name.lower())
        first_name = first_name.replace("'","")
        first_name = first_name.replace("`","")
        if school:
            prefix = len(self.school.prefix)
            username +=  self.school.prefix + "."
        else: 
            prefix = 0
        #Проверки на допустимость
        if len(last_name)+len(first_name)+prefix>28:
            if len(last_name)>25-prefix:
                last_name = last_name[:25-prefix]
                first_name = first_name[:3]
            else:
                if len(last_name)>len(first_name):
                    last_name = last_name[:28-len(first_name)-prefix]
                else:
                    first_name = first_name[:28-len(first_name)-prefix]
        return username + last_name + '.' + first_name
    def save(self, force_insert=False, force_update=False):
        username = self.gen_username()
        try: 
            User.objects.get(username = username)
            self.username = self.gen_username(school = True)
        except:
            self.username = username
        #Пароль по умолчанию
        self.set_password("1")
        super(Clerk, self).save(force_insert, force_update)
    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name', 'middle_name']

class Teacher(Clerk):
    #Для доступа к администраторским функциям (неадмин-панель)
    administrator = models.BooleanField(u"Администратор")
    #Какие предметы ведёт
    subjects = models.ManyToManyField(Subject, verbose_name = u"Предметы", related_name = 'subjects', blank = True, null = True)
    #В каких классах ведёт
    grades = models.ManyToManyField(Grade, blank = True, verbose_name = u"Классы", related_name = "grades", null = True)
    #Есть ли классное руководство
    grade = models.ForeignKey(Grade, verbose_name="Класс", blank = True, related_name = 'grade', null = True)
    #Выбранный предмет в инструменте выставления отметок
    current_subject = models.ForeignKey(Subject, blank = True, related_name = 'current_subject', null = True)
    #Для генерации имени пользователя
    prefix = "t"

class Pupil(Clerk):
    grade = models.ForeignKey(Grade, verbose_name = u"Класс")
    sex = models.CharField(max_length = 1, choices = (('1', u'Юноша'), ('2', u'Девушка')), verbose_name = u'Пол')
    group = models.CharField(max_length = 1, choices = (('1', u'1 группа'), ('2', u'2 группа')), verbose_name = u'Группа')
    #Специальная учебная группа
    special = models.BooleanField(verbose_name = u'Специальная группа')
    prefix = "p"

