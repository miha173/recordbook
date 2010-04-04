# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("src.attendance.views",
                       (r'^$', 'index'),
                       
                       (r'^timetable/select/$', 'timetableSelect'),
                       (r'^timetable/select/(?P<school>\d+)/$', 'timetableSelect'),
                       (r'^timetable/select/(?P<school>\d+)/set/(?P<id>\d+)/$', 'timetableSet'),
                       (r'^timetable/set/(?P<id>\d+)/$', 'timetableSet'),
                       
                       
                       (r'^ringtimetable/$', 'ringtimetableList'),

                       (r'^ringtimetable/new/$', 'ringtimetableList'),
                       (r'^ringtimetable/edit/(?P<id>\d+)/$', 'ringtimetableList'),
                       (r'^ringtimetable/delete/(?P<id>\d+)/$', 'ringtimetableList'),
                       
#                       (r'^ringtimetable/(?P<id>\d+)/$', 'ringList'),
                       )
