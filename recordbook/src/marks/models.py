# -*- coding: UTF-8 -*-

from django.db import models
from src.rest.models import RestModel, RestModelManager
from src.userextended.models import Pupil, Teacher, Subject, Grade, School

class LessonManager(RestModelManager):
    def search(self, str):
        values = []
        a = super(LessonManager, self).get_query_set().filter(grade__long_name__contains = str)
        for obj in a: values.append(obj.id)
        a = super(LessonManager, self).get_query_set().filter(grade__small_name__contains = str)
        for obj in a: values.append(obj.id)
        a = super(LessonManager, self).get_query_set().filter(topic__contains = str)
        for obj in a: values.append(obj.id)
        return super(LessonManager, self).get_query_set().filter(id__in = values)

class Lesson(RestModel):
    objects = LessonManager()
    teacher = models.ForeignKey(Teacher, verbose_name = u'Учитель')
    date = models.DateField(u'Дата')
    topic = models.CharField(u'Тема урока', max_length = 200)
    task = models.CharField(u'Домашнее задание', max_length = 200, blank = True, null = True)
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ManyToManyField(Grade, verbose_name = u'Класс')

    serialize_fields = ['id', 'teacher_id', 'date', 'topic', 'task', 'subject_id', 'grade']
    serialize_name = 'lesson'
    
    class Meta:
        ordering = ['-date']
    def delete(self):
        Mark.objects.filter(lesson = self).delete()
        super(Lesson, self).delete()

class Mark(RestModel):
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    lesson = models.ForeignKey(Lesson, verbose_name = u'Занятие')
    mark = models.IntegerField(u'Отметка', blank = True, null = True)
    absent = models.BooleanField(u'Отсутствовал')
    date = models.DateField(u'Дата выставления', auto_now_add = True)
    comment = models.TextField(u'Комментарий к отметке', blank = True)

    serialize_fields = ['id', 'pupil_id', 'lesson_id', 'mark', 'absent', 'date']
    serialize_name = 'mark'
    
    def get_type(self):
        if self.absent:
            return "bad"
        elif self.mark<3:
            return "bad"
        elif self.mark>=4:
            return "good"
        else:
            return "normal"
    
    def __unicode__(self):
        if self.absent:
            return u'Н'
        else:
            return unicode(self.mark)
    
    class Meta:
        ordering = ['-date']

class ResultDate(RestModel):
    school = models.ForeignKey(School)
    name = models.CharField(max_length=255, verbose_name = u'Имя периода', null = True, blank = True)
    period = models.CharField(u'Итоговый период', max_length = 1, choices = (('1', u'1 четверть'),
                                                                       ('2', u'2 четверть'),
                                                                       ('5', u'1 полугодие'),
                                                                       ('3', u'3 четверть'),
                                                                       ('4', u'4 четверть'),
                                                                       ('6', u'2 полугодие'),
                                                                       ))
    startdate = models.DateField(verbose_name = u'Дата начала периода')
    enddate = models.DateField(verbose_name = u'Дата подведения итога')
    grades = models.ManyToManyField(Grade, verbose_name = u'Классы')

    serialize_fields = ['id', 'name', 'school_id', 'period', 'startdate', 'enddate', 'grades']
    serialize_name = 'resultdate'
    
    class Meta:
        ordering = ['enddate']
    def delete(self):
        Result.objects.filter(resultdate = self).delete()
        super(ResultDate, self).delete()
    def __unicode__(self):
        return self.name

class Result(RestModel):
    resultdate = models.ForeignKey(ResultDate, verbose_name = u'Период')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    mark = models.IntegerField(u'Отметка')

    serialize_fields = ['id', 'resultdate_id', 'subject_id', 'pupil_id', 'mark']
    serialize_name = 'result'
    