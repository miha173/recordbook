# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("odaybook.curatorship.views",
                       (r'^$', 'index'),

                       (r'connections/$', 'connectionsList'),
                       (r'connections/add/$', 'connectionEdit', {'mode': 'add'}),
                       (r'connections/delete/(?P<connection_id>\d+)$', 'connectionEdit', {'mode': 'delete'}),
                       (r'connections/wizard/(?P<step>\d+)/$', 'connectionWizard'),
                       
                       (r'^pupil/$', 'pupilList'),
                       (r'^pupil/add/$', 'pupilEdit', {'mode': 'add'}),
                       (r'^pupil/edit/(?P<id>\d+)/$', 'pupilEdit', {'mode': 'edit'}),
                       (r'^pupil/delete/(?P<id>\d+)/$', 'pupilEdit', {'mode': 'delete'}),
                       
                       (r'pupil_passwords/', 'pupilPasswords'),
                       
                       (r'^graphiks/$', 'graphiks'),
                       )