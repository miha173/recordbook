# -*- coding: UTF-8 -*-

from django.db import models
from odaybook.rest.models import RestModel, RestModelManager
from odaybook.userextended.models import Pupil, Teacher, Subject, Grade, School
from odaybook import settings

class Lesson(RestModel):
    teacher = models.ForeignKey(Teacher, verbose_name = u'Учитель', blank = True, null = True)
    date = models.DateField(u'Дата')
    topic = models.CharField(u'Тема урока', max_length = 200, blank = True, null = True)
    task = models.CharField(u'Домашнее задание', max_length = 200, blank = True, null = True)
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grade = models.ManyToManyField(Grade, verbose_name = u'Класс')
    file = models.FileField(verbose_name = u'Приложить файл', null = True, blank = True, upload_to = 'lessons')
    resultdate = models.ForeignKey('ResultDate', null = True, blank = True)
    fullness = models.BooleanField(default = False)

    serialize_fields = ['id', 'teacher_id', 'date', 'topic', 'task', 'subject_id', 'grade']
    serialize_name = 'lesson'
    
    class Meta:
        ordering = ['-date']

    def save(self, safe = False, *args, **kwargs):
        if not safe and not self.fullness:
            if self.topic and Mark.objects.filter(lesson = self).count()>4:
                self.fullness = True
        super(Lesson, self).save(*args, **kwargs)

class Mark(RestModel):
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    lesson = models.ForeignKey(Lesson, verbose_name = u'Занятие')
    mark = models.IntegerField(u'Отметка', blank = True, null = True)
    absent = models.BooleanField(u'Отсутствовал')
    date = models.DateTimeField(u'Дата выставления', auto_now_add = True)
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
            return u'H'
        else:
            return unicode(self.mark)

    def save(self, *args, **kwargs):
        from odaybook.userextended.models import Notify
        if not self.lesson.fullness:
            if self.lesson.topic and Mark.objects.filter(lesson = self.lesson)>4:
                self.lesson.fullness = True
                self.lesson.save(safe = True)
        super(Mark, self).save(*args, **kwargs)
        Notify.objects.filter(user = self.lesson.teacher, type = '1').delete()
    
    class Meta:
        ordering = ['-date']

class ResultDate(models.Model):
    school = models.ForeignKey(School, null = True, blank = True)
    name = models.CharField(max_length=255, verbose_name = u'Имя периода', null = True, blank = True)
    date = models.DateField(verbose_name = u'Дата подведения итога')
    grades = models.ManyToManyField(Grade, verbose_name = u'Классы')

    def save(self, *args, **kwargs):
        pk = self.pk
        super(ResultDate, self).save(*args, **kwargs)
        if not self.school and not pk:
            from odaybook.userextended.models import School
            for school in School.objects.all():
                ResultDate(school = school, name = self.name, date = self.date).save()

    class Meta:
        ordering = ['date']
    def __unicode__(self):
        return self.name

class Result(RestModel):
    resultdate = models.ForeignKey(ResultDate, verbose_name = u'Период')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик')
    mark = models.IntegerField(u'Отметка')

    serialize_fields = ['id', 'resultdate_id', 'subject_id', 'pupil_id', 'mark']
    serialize_name = 'result'
