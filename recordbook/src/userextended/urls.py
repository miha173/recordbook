# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_change

urlpatterns = patterns("src.userextended.views",
                       (r'login', login, {'template_name': 'userextended/login.html'}),
                       (r'logout', logout, {'next_page': '/'}),
                       (r'password_change', password_change, {'template_name': 'userextended/change_password.html', 'post_change_redirect': '/'}),
                       )