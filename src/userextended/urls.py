# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_change

urlpatterns = patterns("src.userextended.views",
                       (r'^$', 'index'),
                       (r'login', login, {'template_name': 'userextended/login.html'}),
                       (r'logout', logout, {'next_page': '/'}),
                       (r'password_change', password_change, {'template_name': 'userextended/change_password.html', 'post_change_redirect': '/'}),

                       (r'^uni/(?P<object>\w+)/$', 'objectList4Administrator'),
                       (r'^uni/(?P<object>\w+)/add/$', 'objectEdit4Administrator', {'mode': 'add'}),
                       (r'^uni/(?P<object>\w+)/edit/(?P<id>\d+)/$', 'objectEdit4Administrator', {'mode': 'edit'}),
                       (r'^uni/(?P<object>\w+)/delete/(?P<id>\d+)/$', 'objectEdit4Administrator', {'mode': 'delete'}),
                       
                       (r'^uni/(?P<object>\w+)/(?P<school_id>\d+)/$', 'objectList4Administrator'),
                       (r'^uni/(?P<object>\w+)/(?P<school_id>\d+)/add/$', 'objectEdit4Administrator', {'mode': 'add'}),
                       (r'^uni/(?P<object>\w+)/(?P<school_id>\d+)/edit/(?P<id>\d+)/$', 'objectEdit4Administrator', {'mode': 'edit'}),
                       (r'^uni/(?P<object>\w+)/(?P<school_id>\d+)/delete/(?P<id>\d+)/$', 'objectEdit4Administrator', {'mode': 'delete'}),
                       
                       )
