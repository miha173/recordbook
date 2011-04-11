# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("odaybook.attendance.views",
                       (r'^$', 'index'),
                       
                       (r'^timetable/select/$', 'timetableSelect'),
                       (r'^timetable/select/(?P<school>\d+)/$', 'timetableSelect'),
                       (r'^timetable/select/(?P<school>\d+)/set/(?P<id>\d+)/$', 'timetableSet'),
                       (r'^timetable/set/(?P<id>\d+)/$', 'timetableSet'),
                       
                       
                       (r'^ringtimetable/(?P<school>\d+)/$', 'ringtimetableList'),

                       )
