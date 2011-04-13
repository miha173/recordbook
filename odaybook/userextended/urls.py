# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_change

urlpatterns = patterns("odaybook.userextended.views",
                       (r'^$', 'index'),
                       (r'login', login, {'template_name': 'login.html'}),
                       (r'logout', logout, {'next_page': '/'}),
                       (r'password_change', password_change, {'template_name': 'change_password.html',
                                                              'post_change_redirect': '/',
                                                              }),

                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/$', 'objectList'),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/add/$', 'objectEdit', {'mode': 'add'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/edit/(?P<id>\d+)/$', 'objectEdit', {'mode': 'edit'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/delete/(?P<id>\d+)/$', 'objectEdit', {'mode': 'delete'}),

                       # FIXME: дубляж ради school_id очень некрасив
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/$', 'objectList'),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/add/$', 'objectEdit', {'mode': 'add'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/edit/(?P<id>\d+)/$', 'objectEdit', {'mode': 'edit'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/delete/(?P<id>\d+)/$', 'objectEdit', {'mode': 'delete'}),

                       (r'^baseuser/$', 'objectList', {'app': 'userextended', 'model': 'Clerk'}),
                       (r'^baseuser/add/$', 'baseUserObjectEdit', {'mode': 'add'}),
                       (r'^baseuser/edit/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'edit'}),
                       (r'^baseuser/delete/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'delete'}),
                       (r'^baseuser/set/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'set_right'}),
                       (r'^baseuser/dismiss/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'dismiss'}),

                       (r'^set_role/(?P<role_id>\d+)/$', 'set_role'),

                       (r'^appendrole/$', 'clerkAppendRole'),
                       )
