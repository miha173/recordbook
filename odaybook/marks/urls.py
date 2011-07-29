# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("odaybook.marks.views",
                       (r'^$', 'index'),
                       (r'set_current_subject/(?P<subject_id>\d+)', 'set_current_subject'),

                       (r'^subject/(?P<subject_id>\d+)/', 'marksView'),

                       )
