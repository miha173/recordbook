# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_change

urlpatterns = patterns("src.userextended.views",
                       (r'^$', 'index'),
                       (r'login', login, {'template_name': 'userextended/login.html'}),
                       (r'logout', logout, {'next_page': '/'}),
                       (r'password_change', password_change, {'template_name': 'userextended/change_password.html', 'post_change_redirect': '/'}),

                       (r'teacher/$', 'teacherList'),
                       (r'teacher/add/$', 'teacherEdit', {'mode': 'add'}),
                       (r'teacher/edit/(?P<teacher_id>\d+)/$', 'teacherEdit', {'mode': 'edit'}),
                       (r'teacher/delete/(?P<teacher_id>\d+)/$', 'teacherEdit', {'mode': 'delete'}),
                       
                       (r'pupil/$', 'pupilList'),
                       (r'pupil/add/$', 'pupilEdit', {'mode': 'add'}),
                       (r'pupil/edit/(?P<pupil_id>\d+)/$', 'pupilEdit', {'mode': 'edit'}),
                       (r'pupil/delete/(?P<pupil_id>\d+)/$', 'pupilEdit', {'mode': 'delete'}),

#                       (r'(?P<type>\w+)/$', 'gradeList'),

                       
                       (r'subject/$', 'subjectList'),
                       (r'subject/add/$', 'subjectEdit', {'mode': 'add'}),
                       (r'subject/edit/(?P<subject_id>\d+)/$', 'subjectEdit', {'mode': 'edit'}),
                       (r'subject/delete/(?P<subject_id>\d+)/$', 'subjectEdit', {'mode': 'delete'}),
                       
                       (r'grade/$', 'gradeList'),
                       (r'grade/add/$', 'gradeEdit', {'mode': 'add'}),
                       (r'grade/edit/(?P<grade_id>\d+)/$', 'gradeEdit', {'mode': 'edit'}),
                       (r'grade/delete/(?P<grade_id>\d+)/$', 'gradeEdit', {'mode': 'delete'}),
                       )