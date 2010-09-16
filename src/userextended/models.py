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


class School(RestModel):
    u'Модель для школ'
    name = models.CharField(u"Имя учебного заведения", max_length = 100)
    prefix = models.CharField(u"Префикс для логина", max_length = 5)
    saturday = models.BooleanField(verbose_name = u'Шестидневка')
    url = models.URLField(null = True, blank = True)
    address = models.CharField(verbose_name = u'Адрес школы', max_length = 255)
    phone = models.CharField(verbose_name = u'Телефон школы', max_length = 255)
    gate_use = models.BooleanField(verbose_name = u'Использовать шлюз', default = False)
    gate_id = models.CharField(verbose_name = u'ID для SMS-шлюза', max_length = 255, blank = True, null = True)
    gate_password  = models.CharField(verbose_name = u'Пароль для SMS-шлюза', max_length = 255, blank = True, null = True)
    gate_url = models.URLField(verbose_name = u'URL SMS-шлюза', blank = True, null = True, default = 'http://gate.school-record-book.ru')
    max_mark = models.IntegerField(verbose_name = u'Максимальный балл', default = 5)
    gapps_use = models.BooleanField(verbose_name = u'Использовать Google Apps', default = False)
    gapps_login = models.CharField(max_length = 255, default = '', verbose_name = u'Логин для Google Apps', blank = True, null = True)
    gapps_password = models.CharField(max_length = 255, default = '', verbose_name = u'Пароль для Google Apps', blank = True, null = True)
    gapps_domain = models.CharField(max_length = 255, default = '', verbose_name = u'Домен для Google Apps', blank = True, null = True)
    private_domain = models.CharField(max_length = 255, verbose_name = u'Система привязана к домену')
    private_salute = models.CharField(max_length = 255, verbose_name = u'Персональное приветствие')
    

    serialize_fields = ['id', 'name', 'saturday']
    serialize_name = 'school'
    
    def __init__(self, *args, **kwargs):
        from src.marks.models import Mark
        from src.curatorship.models import Connection
        super(School, self).__init__(*args, **kwargs)
        grades = Grade.objects.filter(school = self).count() > 0
        subjects = Subject.objects.filter(school = self).count() > 0
        pupils = Pupil.objects.filter(school = self).count() > 0
        teachers = Teacher.objects.filter(school = self).count() > 0
        marks = Connection.objects.filter(teacher__school = self).count() > 0
        show = {}
        show['teachers'] = show['staff'] = show['subjects'] = show['grades'] = show['cams'] = show['options'] = True
        show['pupils'] = grades
#        show['teachers'] = subjects and grades
        show['resultdates'] = grades
        show['connections'] = teachers
        show['deliveryes'] = marks
        show['timetables'] = teachers
        show['marks'] = marks
        self.show = show
    
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
        Cam.objects.filter(school = self).delete()
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
    number = models.IntegerField(verbose_name = u'Порядковый номер', null = True, blank = True)
    long_name = models.CharField(u"Длинное имя", max_length = 100)
    small_name = models.CharField(u"Короткое имя", max_length = 10, blank = True)
    school = models.ForeignKey(School, verbose_name = "Школа")

    serialize_fields = ['id', 'long_name', 'school_id']
#    serialize_fields = ['id', 'long_name', 'small_name', 'school_id']
    serialize_name = 'grade'
    
    def __unicode__(self):
        if self.number:
            return "%d %s" % (self.number, self.long_name)
        else:
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
    def save(self, *args, **kwargs):
        self.long_name = self.long_name.lower()
        self.small_name = self.small_name.lower()
        super(Grade, self).save(*args, **kwargs)
    class Meta:
        ordering = ['number']

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
    phone = models.CharField(max_length = 20, verbose_name = u'Номер телефона', null = True, blank = True)
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
        def _clean_name(name):
            '''Чистка фамилии и имени от инородных символов и транслитерация'''
            name = pytils.translit.translify(self.name.lower())
            name = name.replace("'","")
            name = name.replace("`","").strip()
            name = name.replace(' ', '_')

        username = self.prefix + "."
        #Удаление нехороших символов из траслитерации
        last_name = _clean_name(last_name)
        first_name = _clean_name(first_name)
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
    def save(self, force_insert = False, force_update = False, init = False, safe = False):
        if hasattr(self, 'account'): self.account = str(self.account)
        if self.pk:
            if self.prefix == 'p':
                old = Pupil.objects.get(id = self.id)
            if self.prefix == 't':
                old = Teacher.objects.get(id = self.id)
            if self.prefix == 's':
                old = Staff.objects.get(id = self.id)
        if self.school.gate_use:
            from gate import Gate
            gate = Gate(self.school.gate_url, self.school.gate_id, self.school.gate_password)
            if self.prefix == 'p':
                if not self.gate_id:
                    if len(self.phone_mother) > 5:
                        self.gate_id = gate.addUser(self.phone_mother)
                    if len(self.phone_father) > 5:
                        self.gate_id = gate.addUser(self.phone_father)
                else:
                    if old.phone_mother != self.phone_mother:
                        gate.changePhone(self.gate_id, self.phone_mother)
                    if old.phone_father != self.phone_father:
                        gate.changePhone(self.gate_id, self.phone_father)
        if not self.pk or init:
            if self.school.gapps_use:
                import gdata.apps.service
                self.username = self.gen_username()
                service = gdata.apps.service.AppsService(email = self.school.gapps_login, domain = self.school.gapps_domain, password = self.school.gapps_password)
                service.ProgrammaticLogin()
                try:
                    service.CreateUser(self.username, self.last_name, self.first_name, '123456789', quota_limit=1000)
                except gdata.apps.service.AppsForYourDomainException, (error, ):
                    self.set_password('123456789')
                    super(Clerk, self).save(force_insert, force_update)
                    raise gdata.apps.service.AppsForYourDomainException(error)
            else: 
                from random import randint
                username = self.school.prefix + str(randint(10**6, 9999999))
                while User.objects.filter(username = username).count()!=0:
                    username = '39' + str(randint(10**6, 9999999))
                self.username = username
            self.set_password("123456789")
            super(Clerk, self).save(force_insert, force_update)
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
    # Для доступа к администраторским функциям 
    administrator = models.BooleanField(u"Администратор")
    # Какие предметы ведёт
    subjects = models.ManyToManyField(Subject, verbose_name = u"Предметы", related_name = 'subjects', blank = True, null = True)
    # В каких классах ведёт
    grades = models.ManyToManyField(Grade, blank = True, verbose_name = u"Классы", related_name = "grades", null = True)
    # Есть ли классное руководство
    grade = models.ForeignKey(Grade, verbose_name="Класс", blank = True, related_name = 'grade', null = True)
    # Выбранный предмет в инструменте выставления отметок
    current_subject = models.ForeignKey(Subject, blank = True, related_name = 'current_subject', null = True)
    # Для генерации имени пользователя и других костылей
    prefix = "t"

    serialize_fields = ['id', 'last_name', 'first_name', 'middle_name', 'grade_id', 'school_id', 'grades', 'subjects']
    serialize_name = 'teacher'
    
    def is_administrator(self):
        return self.is_superuser or self.is_staff or self.administrator

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
    account = models.DecimalField(verbose_name = u'Баланс', default = '0', max_digits = 20, decimal_places = 2)
    parent_mother = models.CharField(max_length = 255, verbose_name = u'Мать', blank = True, null = True)
    parent_father = models.CharField(max_length = 255, verbose_name = u'Отец', blank = True, null = True)
    phone_mother = models.CharField(max_length = 255, verbose_name = u'Телефон матери', blank = True, null = True)
    phone_father = models.CharField(max_length = 255, verbose_name = u'Телефон отца', blank = True, null = True)
    delivery = models.BooleanField(default = True, verbose_name = u'Отправлять SMS')
    insurance_policy = models.TextField(verbose_name = u'Страховой полис', null = True, blank = True)
    gate_id = models.IntegerField(null = True, blank = True)
    
    prefix = "p"
    serialize_fields = ['id', 'cart', 'account', 'last_name', 'first_name', 'middle_name', 'grade_id', 'group', 'school_id']
    serialize_name = 'pupil'
    
    def curator(self):
        teacher = Teacher.objects.filter(grade = self.grade)
        if teacher.count() == 0:
            return Teacher(grade = self.grade, last_name = '', first_name = '', middle_name = '')
        else:
            return teacher[0]
    
    def get_marks_avg(self, delta = timedelta(weeks = 4)):
        from decimal import *
        from src.marks.models import Mark
        temp = Mark.objects.filter(pupil = self, absent = False, lesson__date__gte = datetime.now()-delta).aggregate(Avg('mark'))['mark__avg']
        if not temp:
            temp = 0
        getcontext().prec = 2
#        temp = Decimal(str(temp))
        return "%.2f" % temp
    def get_marks_avg_type(self, delta = timedelta(weeks = 4)):
        mark = self.get_marks_avg(delta)
        if mark<3:
            return "bad"
        elif mark>=4:
            return "good"
        else:
            return "normal"
    def get_teachers(self):
        from src.curatorship.models import Connection
        teachers = set([connection.teacher for connection in Connection.objects.filter(grade = self.grade) if connection.connection == '0' or connection.connection == self.group or (int(connection.connection)-2) == self.sex or (int(connection.connection)-4) == int(self.special)])
        return teachers
    def get_subjects(self):
        from src.curatorship.models import Connection
        return [connection.subject for connection in Connection.objects.filter(grade = self.grade) if connection.connection == '0' or connection.connection == self.group or (int(connection.connection)-2) == self.sex or (int(connection.connection)-4) == int(self.special)]

    def is_administrator(self):
        return False

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
    
    # Для доступа к администраторским функциям 
    administrator = models.BooleanField(u"Администратор", default = False)

    def is_administrator(self):
        return self.is_superuser or self.is_staff or self.administrator

class Permission(models.Model):
    user_id = models.IntegerField()
    user_type = models.CharField(max_length = 1, choices = (('p', 'p'), ('t', 't'), ('s', 's')))
    permission = models.CharField(max_length = 255)

    def user(self):
        if self.user_type == 'p': Model = Pupil
        elif self.user_type == 't': Model = Teacher
        elif self.user_type == 's': Model = Staff
        return Model.objects.get(id = self.user_id)



