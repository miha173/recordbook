from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       (r"^$", "lyc01.views.index"),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^(?P<application>[a-z]+)/pages/(?P<pageid>\d+)$', 'lyc01.pages.views.get'),
                       (r'^press/', 'lyc01.press.views.main'),
                       (r'^probe/', 'lyc01.userextended.views.main')
)
