# -*- coding: UTF-8 -*-

from datetime import timedelta, datetime

from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Avg
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pytils

from src.rest.models import RestModel, RestModelManager
from src.utils import PlaningError



def Hex2Bin(ch):
    ch = ch.upper()
    if ch == '0': return '0000'
    elif ch == '1': return '0001'
    elif ch == '2': return '0010'
    elif ch == '3': return '0011'
    elif ch == '4': return '0100'
    elif ch == '5': return '0101'
    elif ch == '6': return '0110'
    elif ch == '7': return '0111'
    elif ch == '8': return '1000'
    elif ch == '9': return '1001'
    elif ch == 'A': return '1010'
    elif ch == 'B': return '1011'
    elif ch == 'C': return '1100'
    elif ch == 'D': return '1101'
    elif ch == 'E': return '1110'
    elif ch == 'F': return '1111'

def Bin2Hex(ch):
    ch = ch.upper()
#    print ch
    if ch == '0000': return '0'
    elif ch == '0001': return '1'
    elif ch == '0010': return '2'
    elif ch == '0011': return '3'
    elif ch == '0100': return '4'
    elif ch == '0101': return '5'
    elif ch == '0110': return '6'
    elif ch == '0111': return '7'
    elif ch == '1000': return '8'
    elif ch == '1001': return '9'
    elif ch == '1010': return 'A'
    elif ch == '1011': return 'B'
    elif ch == '1100': return 'C'
    elif ch == '1101': return 'D'
    elif ch == '1110': return 'E'
    elif ch == '1111': return 'F'




class School(RestModel):
    u'Модель для школ'
    name = models.CharField(u"Имя учебного заведения", max_length = 100)
    prefix = models.CharField(u"Префикс для логина", max_length = 5)
    saturday = models.BooleanField(verbose_name = u'Шестидневка')
    url = models.URLField(null = True, blank = True)
    address = models.CharField(verbose_name = u'Адрес школы', max_length = 255)
    phone = models.CharField(verbose_name = u'Телефон школы', max_length = 255)

    serialize_fields = ['id', 'name', 'saturday']
    serialize_name = 'school'
    
    def __unicode__(self):
        return self.name
    def get_workdays(self):
        if self.saturday:
            days = 6
        else:
            days = 5
        return xrange(1, days+1)
    def delete(self):
        from src.marks.models import ResultDate
        Grade.objects.filter(school = self).delete()
        Subject.objects.filter(school = self).delete()
        Teacher.objects.filter(school = self).delete()
        Pupil.objects.filter(school = self).delete()
        ResultDate.objects.filter(school = self).delete()
        Cam.objects.filter(school = school).delete()
        super(School, self).delete()

class Cam(models.Model):
    name = models.CharField(max_length = 255, verbose_name = u'Название камеры')
    ip = models.IPAddressField(verbose_name = u'IP камеры')
    device1 = models.CharField(max_length = 255, verbose_name = u'Устройство 1', null = True, blank = True)
    device1_name = models.CharField(max_length = 255, verbose_name = u'Устройство 1 - имя', null = True, blank = True)
    device2 = models.CharField(max_length = 255, verbose_name = u'Устройство 2', null = True, blank = True)
    device2_name = models.CharField(max_length = 255, verbose_name = u'Устройство 2 - имя', null = True, blank = True)
    school = models.ForeignKey(School, verbose_name = u'Школа')

class Option(models.Model):
    key = models.CharField(max_length = 255, verbose_name = u'Настройка')
    value = models.CharField(max_length = 255, verbose_name = u'Значение')
    school = models.ForeignKey(School, verbose_name = u'Школа')


class Grade(RestModel):
    u'Классы в школах'
    long_name = models.CharField(u"Длинное имя", max_length = 100)
    small_name = models.CharField(u"Короткое имя", max_length = 10, blank = True)
    school = models.ForeignKey(School, verbose_name = "Школа")

    serialize_fields = ['id', 'long_name', 'school_id']
#    serialize_fields = ['id', 'long_name', 'small_name', 'school_id']
    serialize_name = 'grade'
    
    def __unicode__(self):
        return self.long_name
    def get_subjects(self):
        from src.curatorship.models import Connection
        subjects = []
        for t in Teacher.objects.filter(grades = self):
            subjects += [subj.id for subj in t.subjects.all()]
        temp = Subject.objects.filter(id__in = subjects)
        return temp
        #temp = [1, 2, 3]
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
            raise PlaningError(u"В классе числятся ученики")
    class Meta:
        ordering = ['long_name']

class Subject(RestModel):
    u'Учебные дисциплины'
    name = models.CharField(u"Наименование", max_length = 100)
    school = models.ForeignKey(School, verbose_name = "Школа")

    serialize_fields = ['id', 'name', 'school_id']
    serialize_name = 'subject'
    
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

class ClerkManager(RestModelManager):
    def __init__(self, fields):
        self.search_fields = fields
        models.Manager.__init__(self)
    def search(self, str):
        from django.db.models import Q
        search_query_list = [Q(**{s + '__icontains': str}) for s in self.search_fields]
        search_query = reduce(lambda x, y: x | y, search_query_list)
        return self.filter(search_query)

class Clerk(User, RestModel):
    u'Базовый класс расширенного пользователя. Потомки - учителя, ученики.'
    objects = ClerkManager(['last_name', 'first_name', 'middle_name', 'grade__long_name', 'grade__small_name'])
    middle_name = models.CharField(u"Отчество", max_length = 30, blank = True)
    password_journal = models.CharField(u"Пароль доступа к дневнику", max_length = 255)
    school = models.ForeignKey(School, verbose_name = "Школа")
    cart = models.CharField(u'Карта', max_length = 10, null = True, blank = True)
    cart_ext = models.CharField(u'Карта (рат.)', max_length = 10, null = True, blank = True)
    def __unicode__(self):
        result = self.last_name + ' ' + self.first_name + ' ' + self.middle_name
#        if self.grade:
#            result = result + ' (' + self.grade.small_name + ')'
        return result
    def fio(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name
    #Вывод строки "Фамилия Имя"
    def fi(self):
        return self.last_name + ' ' + self.first_name
    #Вывод строки "Имя Фамилия"
    def if_(self):
        return self.first_name + ' ' + self.last_name
    def get_fio(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.middle_name)
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
    def save(self, force_insert = False, force_update = False, init = False):
        from src.settings import GAPPS_DOMAIN, GAPPS_LOGIN, GAPPS_PASSWORD, GAPPS_USE, USE_SHELNI
        if not self.cart: self.cart = ''
        if self.cart[len(self.cart)-4:len(self.cart)] == '001A':
            cart = self.cart[:len(self.cart)-4]
            cart = "".join([Hex2Bin(i) for i in cart])
            new_cart = "".join([cart[i] for i in xrange(len(cart)-1, -1, -1)])
            new_cart = "".join([Bin2Hex(new_cart[i-4:i]) for i in xrange(4, len(new_cart)+1, 4)])
            new_cart = "".join([new_cart[i-2:i] for i in xrange(len(new_cart), 0, -2)])
            self.cart_ext = new_cart + '001A'
        if USE_SHELNI:
            from shelni import ShelniConfig
            tc_ip = Option.objects.get(key = 'TC_IP')
            cams = []
            for cam in Cam.objects.filter(school = self.school):
                cams.append([cam.device1, 1])
                cams.append([cam.device2, 1])
            c = ShelniConfig(host = tc_ip.value, devices = cams)
            c.login('Serega', '1')
        if not self.pk or init:
#            if not init:
#                username = self.gen_username()
#                if User.objects.filter(username = username).count() != 0:
#                    self.username = self.gen_username(school = True)
            if GAPPS_USE:
                import gdata.apps.service
                service = gdata.apps.service.AppsService(email=GAPPS_LOGIN, domain=GAPPS_DOMAIN, password=GAPPS_PASSWORD)
                service.ProgrammaticLogin()
                service.CreateUser(self.username, self.last_name, self.first_name, '123456789', quota_limit=1000)
            else: 
                from random import randint
                username = self.school.prefix + str(randint(10**6, 9999999))
                while User.objects.filter(username = username).count()!=0:
                    username = '39' + str(randint(10**6, 9999999))
                self.username = username
            self.set_password("123456789")
            super(Clerk, self).save(force_insert, force_update)
            if USE_SHELNI:
                c.add_user(self.cart_ext, cell = self.id)
        else:
            if USE_SHELNI:
                c.add_user(self.cart_ext, cell = self.id)
            super(Clerk, self).save(force_insert, force_update)
    def search(self, search_str):
        values = []
        a = self.objects.filter(last_name__contains = search_str)
        for obj in a: values.append(obj)
        return values
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

    serialize_fields = ['id', 'last_name', 'first_name', 'middle_name', 'grade_id', 'school_id', 'grades', 'subjects']
    serialize_name = 'teacher'
    
    def is_administrator(self):
        return self.is_staff or self.administrator

    def delete(self):
        from src.marks.models import Lesson
        Lesson.objects.filter(teacher = self).delete()
        super(Teacher, self).delete()

class Pupil(Clerk):
    grade = models.ForeignKey(Grade, verbose_name = u"Класс")
    sex = models.CharField(max_length = 1, choices = (('1', u'Юноша'), ('2', u'Девушка')), verbose_name = u'Пол')
    group = models.CharField(max_length = 1, choices = (('1', u'1 группа'), ('2', u'2 группа')), verbose_name = u'Группа')
    #Специальная учебная группа
    special = models.BooleanField(verbose_name = u'Специальная группа')
    account = models.FloatField(verbose_name = u'Баланс', default = 0)
    parent_mother = models.CharField(max_length = 255, verbose_name = u'Мать', blank = True, null = True)
    parent_father = models.CharField(max_length = 255, verbose_name = u'Отец', blank = True, null = True)
    phone_mother = models.CharField(max_length = 255, verbose_name = u'Телефон матери', blank = True, null = True)
    phone_father = models.CharField(max_length = 255, verbose_name = u'Телефон отца', blank = True, null = True)
    delivery = models.BooleanField(default = True, verbose_name = u'Отправлять смс')
    
    prefix = "p"
    serialize_fields = ['id', 'last_name', 'first_name', 'middle_name', 'grade_id', 'group', 'school_id']
    serialize_name = 'pupil'
    
    def curator(self):
        return Teacher.objects.get(grade = self.grade)
    
    def get_marks_avg(self, delta = timedelta(weeks = 4)):
        from decimal import *
        from src.marks.models import Mark
        temp = Mark.objects.filter(pupil = self, absent = False, lesson__date__gte = datetime.now()-delta).aggregate(Avg('mark'))['mark__avg']
        if not temp:
            temp = 0
        getcontext().prec = 4
        temp = Decimal(str(temp))
        return temp    
    def get_marks_avg_type(self, delta = timedelta(weeks = 4)):
        mark = self.get_marks_avg(delta)
        if mark<3:
            return "bad"
        elif mark>=4:
            return "good"
        else:
            return "normal"
    def get_teachers(self):
#        from src.curatorship.models import Connection
#        teachers = [connection.teacher for connection in Connection.objects.filter(grade = self.grade) if connection.connection == '0' or connection.connection == self.group or (int(connection.connection)-2) == self.sex or (int(connection.connection)-4) == int(self.special)]
#        for teacher in teachers:
#            ok = False
#            for i in xrange(len(teachers)-1):
#                if teachers[i].id == teacher.id:
#                    if ok:
#                        del teachers[i]
#                    else: ok = True
        teachers = Teacher.objects.filter(grades = self.grade)
        return teachers
    def get_subjects(self):
        subjects = set()
        for teacher in self.get_teachers():
            for sbj in teacher.subjects.all():
                subjects.add(sbj)
        return subjects
#        from src.curatorship.models import Connection
#        return [connection.subject for connection in Connection.objects.filter(grade = self.grade) if connection.connection == '0' or connection.connection == self.group or (int(connection.connection)-2) == self.sex or (int(connection.connection)-4) == int(self.special)]

class Achievement(models.Model):
    title = models.CharField(verbose_name = u'Достижение', max_length = 255)
    description = models.TextField(verbose_name = u'Описание достижения')
    date = models.DateField(verbose_name = u'Дата')
    pupil = models.ForeignKey(Pupil)

class Staff(Clerk):
    '''
    Модель персонала
    '''
    prefix = 's'
