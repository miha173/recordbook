# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^chaining/', include('smart_selects.urls')),
                       (r"^$", "src.views.index"),
                       (r"^grade/$", "src.views.grade"),
                       (r"^subjects/$", "src.views.subjects"),
                       (r"^teachers/$", "src.views.teachers"),
                       (r"^teachers/(?P<id>\d+)/$", "src.views.teacher"),
                       (r"^sms/$", "src.views.sms"),
                       
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       
                       (r'^accounts/', include('src.userextended.urls')),
                       (r'^marks/', include('src.marks.urls')),
                       (r'^curatorship/', include('src.curatorship.urls')),
                       (r'^administrator/', include('src.userextended.urls')),
                       (r'^attendance/', include('src.attendance.urls')),
                       (r'^api/', include('src.api.urls')),
)
