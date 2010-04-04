# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin

from src.settings import REST_MODELS, MARKS_SECRET_KEY

urlpatterns = patterns('src.api.views',
#                       (r"^$", 'REST'),
                       (r"^terminal/main/$", "terminalMain"),
                       (r"^terminal/marks/$", "terminalMarks"),
                       (r"^terminal/book/$", "terminalBook"),
                       (r'^syncdb/$', 'syncdb')
                       
)


for model in REST_MODELS:
    urlpatterns += patterns('src.api.views', 
                           (r"^%s/$" % model, "REST", {'model': model}),
                           (r"^%s/(?P<id>\d+)/$" % model, "REST", {'model': model}), 
                            )
