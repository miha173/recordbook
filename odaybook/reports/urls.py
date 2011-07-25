# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("odaybook.reports.views",
                       (r'^$', 'index'),
                       (r'^health/$', 'report_health'),
                       (r'^order/$', 'report_order'),
                       (r'^fillability/$', 'report_fillability'),
                       (r'^membershipchanges/$', 'report_membershipchanges'),
                       )
