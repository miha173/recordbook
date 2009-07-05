# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns("src.curatorship.views",
                       (r'^$', 'index'),
                       (r'connections/$', 'connectionsList'),
                       (r'connections/add/$', 'connectionEdit', {'mode': 'add'}),
                       (r'connections/delete/(?P<connection_id>\d+)$', 'connectionEdit', {'mode': 'delete'}),
                       (r'connections/wizard/(?P<step>\d+)/$', 'connectionWizard'),
                       
                       (r'pupil_passwords/', 'pupilPasswords')
                       )