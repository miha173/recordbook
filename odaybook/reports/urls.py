# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns

urlpatterns = patterns("odaybook.reports.views",
                       (r'^$', 'index'),
                       (r'^health/$', 'report_health'),
                       (r'^order/$', 'report_order'),
                       (r'^fillability/$', 'report_fillability'),
                       (r'^membershipchanges/$', 'report_membershipchanges'),
                       (r'^marks/$', 'report_marks'),
                       (r'^marks/(?P<id>\d+)/$', 'view_marks'),
                       (r'^marks/result/$', 'report_marks', {'mode': 'result'}),
                       )
