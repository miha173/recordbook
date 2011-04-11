# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin

from odaybook.settings import REST_MODELS

urlpatterns = patterns('odaybook.api.views',
                       (r'^permissions/$', 'permissions'),
                       
)


for model in REST_MODELS:
    urlpatterns += patterns('odaybook.api.views', 
                           (r"^%s/$" % model, "REST", {'model': model}),
                           (r"^%s/(?P<id>\d+)/$" % model, "REST", {'model': model}), 
                            )
