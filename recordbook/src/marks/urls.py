# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("src.marks.views",
                       (r'^$', 'index'),
                       (r'^(?P<id>\d+)/$', 'viewMarks'),
                       (r'set_current_subject/(?P<subject_id>\d+)', 'set_current_subject'),
                       
                       (r'^lesson/$', 'lessonList'),
                       (r'^lesson/add/$', 'lessonEdit', {'mode': 'add'}),
                       (r'^lesson/edit/(?P<id>\d+)/$', 'lessonEdit', {'mode': 'edit'}),
                       (r'^lesson/delete/(?P<id>\d+)/$', 'lessonEdit', {'mode': 'delete'}),

                       (r'^grade/$', 'gradeList'),
                       (r'^grade/(?P<grade_id>\d+)/$', 'gradeLessonList'),
                       (r'^grade/(?P<grade_id>\d+)/(?P<lesson_id>\d+)/$', 'markList'),
                       (r'^grade/(?P<grade_id>\d+)/(?P<lesson_id>\d+)/give/$', 'giveMark'),
                       
                       (r'^result/$', 'gradeResultList'),
                       (r'^result/give/$', 'gradeResult'),
                       
                       (r'^subject/(?P<subject_id>\d+)/', 'marksView'),
                       )