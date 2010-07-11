from django.conf.urls.defaults import *

urlpatterns = patterns('smart_selects.views',
    url(r'^(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filterchain', name='chained_filter'),
    url(r'^simple/(?P<app>[\w\-]+)/(?P<model>[\w\-]+)/(?P<field>[\w\-]+)/(?P<value>[\w\-]+)/$', 'filtersimplechain', name='simplechained_filter'),
)
