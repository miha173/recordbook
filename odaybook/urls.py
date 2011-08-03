# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   (r'^chaining/', include('smart_selects.urls')),
   (r"^$", "odaybook.views.index"),
   (r"^grade/$", "odaybook.views.grade"),
   (r"^subjects/$", "odaybook.views.subjects"),
   (r"^teachers/$", "odaybook.views.teachers"),
   (r"^teachers/(?P<id>\d+)/$", "odaybook.views.teacher"),

   (r'^admin/doc/', include('django.contrib.admindocs.urls')),
   (r'^admin/(.*)', include(admin.site.urls)),

   (r'^accounts/', include('odaybook.userextended.urls')),
   (r'^marks/', include('odaybook.marks.urls')),
   (r'^curatorship/', include('odaybook.curatorship.urls')),
   (r'^administrator/', include('odaybook.userextended.urls')),
   (r'^attendance/', include('odaybook.attendance.urls')),
   (r'^reports/', include('odaybook.reports.urls')),
)
