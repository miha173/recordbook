# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns

urlpatterns = patterns("odaybook.curatorship.views",
   (r'^$', 'index'),

   (r'connections/$', 'connections_list'),
   (r'connections/add/$', 'connection_edit', {'mode': 'add'}),
   (r'connections/delete/(?P<connection_id>\d+)$', 'connection_edit', {'mode': 'delete'}),

   (r'^pupil/$', 'pupil_list'),
   (r'^pupil/add/$', 'pupil_edit', {'mode': 'add'}),
   (r'^pupil/edit/(?P<id>\d+)/$', 'pupil_edit', {'mode': 'edit'}),
   (r'^pupil/delete/(?P<id>\d+)/$', 'pupil_edit', {'mode': 'delete'}),

   (r'^send-append-request/$', 'send_parent_request'),

   (r'^requests/approve/$', 'requests', {'mode': 'approve'}),
   (r'^requests/disapprove/$', 'requests', {'mode': 'disapprove'}),
)