# -*- coding: UTF-8 -*-

from django.db import models

from src.userextended.models import Subject, Grade, Teacher, Pupil

class Test(models.Model):
    teacher = models.ForeignKey(Teacher, related_name = 'teacher')
    name = models.CharField(max_length = 255, verbose_name = u'Название теста')
    subject = models.ForeignKey(Subject, verbose_name = u'Предмет')
    grades = models.ManyToManyField(Grade, verbose_name = u'Классы')
    mark5 = models.IntegerField(verbose_name = u'Баллов на 5')
    mark4 = models.IntegerField(verbose_name = u'Баллов на 4')
    mark3 = models.IntegerField(verbose_name = u'Баллов на 3')
    share = models.ManyToManyField(Teacher, blank = True, null = True)
    public = models.DateTimeField(verbose_name = "Время публикации", blank = True, null = True)
    def delete(self):
        QuestionA.objects.filter(test = self).delete()
        QuestionB.objects.filter(test = self).delete()
        Result.objects.filter(test = self).delete()

class Question(models.Model):
    name = models.CharField(max_length = 250, verbose_name = u'Тема вопроса')
    type = models.CharField(max_length = 1, choices = ( ('A', 'A'), ('B', 'B') ))
    test = models.ForeignKey(Test, verbose_name = u'Тест')
    number = models.IntegerField(verbose_name = u'Номер вопроса')

class Variant(models.Model):
    question = models.ForeignKey(Question)
    task = models.TextField(verbose_name = u'Вопрос')
    answer = models.CharField(max_length = 100, verbose_name = 'Правильный ответ')
    class Meta:
        abstract = True
        ordering = ['question__number']

class VariantA(Variant):
    option1 = models.CharField(max_length = 100, verbose_name = u'Вариант ответа 1')
    option2 = models.CharField(max_length = 100, verbose_name = u'Вариант ответа 2')
    option3 = models.CharField(max_length = 100, verbose_name = u'Вариант ответа 3')
    option4 = models.CharField(max_length = 100, verbose_name = u'Вариант ответа 4')

class VariantB(Variant):
    pass

class Result(models.Model):
    pupil = models.ForeignKey(Pupil, verbose_name = u'Ученик', related_name = "pupil")
    test = models.ForeignKey(Test, verbose_name = u'Тест')
    mark = models.IntegerField(verbose_name = u'Количество баллов')
    questionA = models.TextField()
    questionB = models.TextField()
    answersA = models.TextField(verbose_name = u'Ответы части A')
    answersB = models.TextField(verbose_name = u'Ответы части B')
    start = models.DateTimeField()
    end = models.DateTimeField(auto_now_add = True)

