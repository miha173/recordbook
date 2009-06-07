# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       (r"^$", "src.views.index"),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^accounts/', include('src.userextended.urls')),
                       (r'^marks/', include('src.marks.urls'))
)
