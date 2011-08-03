# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns
from django.contrib.auth.views import login, logout, password_change, \
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from forms import PasswordChangeForm

urlpatterns = patterns("odaybook.userextended.views",
                       (r'^$', 'index'),
                       (r'login', login, {'template_name': 'login.html'}),
                       (r'logout', logout, {'next_page': '/'}),
                       (r'password_change', password_change, {'template_name': 'change_password.html',
                                                              'post_change_redirect': '/',
                                                              'password_change_form': PasswordChangeForm,
                                                              }),
                       (r'password_reset/$', password_reset, {'template_name': 'password_reset.html',}),
                       (r'password_reset_done/$', password_reset_done, {'template_name': 'password_reset_done.html'}),
                       (r'password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
                        {'template_name': 'password_reset_confirm.html',}),

                       (r'password_reset_complete/$', password_reset_complete,
                        {'template_name': 'password_reset_complete.html',}),

                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/$', 'objectList'),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/add/$', 'objectEdit', {'mode': 'add'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/edit/(?P<id>\d+)/$', 'objectEdit', {'mode': 'edit'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/delete/(?P<id>\d+)/$', 'objectEdit', {'mode': 'delete'}),

                       # дубляж ради filter_id очень некрасив
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/$', 'objectList'),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/add/$', 'objectEdit', {'mode': 'add'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/edit/(?P<id>\d+)/$',
                        'objectEdit', {'mode': 'edit'}),
                       (r'^uni/(?P<app>\w+).(?P<model>\w+)/(?P<filter_id>\d+)/delete/(?P<id>\d+)/$',
                        'objectEdit', {'mode': 'delete'}),

                       (r'^baseuser/$', 'objectList', {'app': 'userextended', 'model': 'Clerk'}),
                       (r'^baseuser/add/$', 'baseUserObjectEdit', {'mode': 'add'}),
                       (r'^baseuser/edit/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'edit'}),
                       (r'^baseuser/delete/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'delete'}),
                       (r'^baseuser/set/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'set_right'}),
                       (r'^baseuser/dismiss/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'dismiss'}),
                       (r'^baseuser/reset_password/(?P<id>\d+)/$', 'baseUserObjectEdit', {'mode': 'reset_password'}),
                       
                       (r'^uni/userextended.Grade/(?P<filter_id>\d+)/import/$', 'import_grade'),
                       (r'^uni/userextended.Teacher/(?P<filter_id>\d+)/import/$', 'import_teacher'),
                       (r'^uni/userextended.Pupil/(?P<filter_id>\d+)/import/$', 'import_pupil'),

                       (r'^set_role/(?P<role_id>\d+)/$', 'set_role'),
                       (r'^set_current_pupil/(?P<id>\d+)/$', 'set_current_pupil'),

                       (r'^appendrole/$', 'clerkAppendRole'),
                       (r'^register-clerk/$', 'register_clerk'),

                       (r'^ajax/get/subject/(?P<id>\d+)/$', 'get_subject'),
                       
                       (r'^uni/userextended.Pupil/(?P<filter_id>\d+)/exclude/(?P<id>\d+)/$', 'exclude_pupil'),
                       (r'^uni/userextended.Pupil/(?P<school>\d+)/connect/$', 'connect_pupil'),
                       )
