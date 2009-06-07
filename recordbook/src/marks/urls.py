# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.views.generic import list_detail
from src.marks.models import Lesson
from src.marks.views import lesson

urlpatterns = patterns("src.marks.views",
                       (r'^$', 'index'),
                       (r'set_current_subject/(?P<subject_id>\d+)', 'set_current_subject'),
                       (r'lessons$', list_detail.object_list, {'queryset': Lesson.objects.all(),
                                                             'template_name': 'marks/teacher/lessons.html',
                                                             'template_object_name': 'lessons'}),
                       (r'lessons/add', 'lesson', {'mode': 'add'}),
                       (r'lessons/edit/(?P<id>\d+)', 'lesson', {'mode': 'edit'}),
                       )