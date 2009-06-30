# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("src.marks.views",
                       (r'^$', 'index'),
                       (r'set_current_subject/(?P<subject_id>\d+)', 'set_current_subject'),
                       (r'lessons/$', 'lessonsList'),
                       (r'lessons/add/$', 'lessonEdit', {'mode': 'add'}),
                       (r'lessons/edit/(?P<id>\d+)/$', 'lessonEdit', {'mode': 'edit'}),
                       (r'lessons/delete/(?P<id>\d+)/$', 'lessonEdit', {'mode': 'delete'}),
                       (r'grades/$', 'gradesList'),
                       (r'grades/(?P<grade_id>\d+)/$', 'gradeLessonsList'),
                       (r'grades/(?P<grade_id>\d+)/(?P<lesson_id>\d+)/$', 'marksList'),
                       )