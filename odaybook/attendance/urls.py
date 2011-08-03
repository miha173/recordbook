# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns

urlpatterns = patterns("odaybook.attendance.views",
                       (r'^$', 'index'),
                       
                       (r'^timetable/select/$', 'timetable_select'),
                       (r'^timetable/select/(?P<school>\d+)/$', 'timetable_select'),
                       (r'^timetable/select/(?P<school>\d+)/import/$', 'import_timetable'),
                       (r'^timetable/select/(?P<school>\d+)/set/(?P<id>\d+)/$', 'timetable_set'),
                       (r'^timetable/set/(?P<id>\d+)/$', 'timetable_set'),
                       
                       

                       )
