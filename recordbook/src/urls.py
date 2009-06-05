from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       (r"^$", "src.views.index"),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^probe/', 'src.userextended.views.main')
)
