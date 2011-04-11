# -*- coding: UTF-8 -*-

from django.contrib.auth import get_user
from django.http import HttpResponse
from django.shortcuts import render_to_response

from models import Pupil, Teacher, Staff, School, Option, BaseUser, Clerk, Parent, Superviser

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            user = get_user(request);
            userprofile = user
            if user.is_authenticated():
                try:
                    userprofile = Clerk.objects.get(user_ptr = user)
                    if userprofile.current_role:
                        userprofile.type = userprofile.current_role.type
                    elif userprofile.is_superuser:
                        userprofile.type = 'Superuser'
                    if userprofile.current_role:
                        userprofile.c = userprofile.current_role.c
                except Clerk.DoesNotExist:
                    userprofile = user
                    userprofile.type = 'Anonymous'
            else:
                if School.objects.filter(private_domain = request.META['HTTP_HOST']):
                    userprofile.private_salute = School.objects.filter(private_domain = request.META['HTTP_HOST'])[0].private_salute
            request._cached_user = userprofile
        return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()
        return None
