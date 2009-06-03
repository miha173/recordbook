# -*- coding: UTF-8 -*-

from django.db import models
from django.conf import settings

class Novetly(models.Model):
    u'Обычная текстовая новость'
    title = models.CharField(u"Заголовок", max_length = 250)
    date = models.DateField(auto_now_add = True)
    text = models.TextField(u"Текст")

class Paper(models.Model):
    title = models.CharField(max_length = 250)
    date = models.DateField(auto_now_add = True)
    file = models.FileField(upload_to = settings.MEDIA_ROOT)

class PhotoAlbum(models.Model):
    title = models.CharField(max_length = 250)
    date = models.DateField(auto_now_add = True)
    picassaid = models.CharField(max_length = 250)

class Document(models.Model):
    title = models.CharField(max_length = 250)
    date = models.DateField(auto_now_add = True)
    file = models.FileField(upload_to = settings.MEDIA_ROOT)
