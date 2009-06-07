# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns("src.userextended.views",
                       (r'login', login, {'template_name': 'userextended/login.html'}),
                       (r'logout', logout, {'next_page': '/accounts/login'}),
                       )