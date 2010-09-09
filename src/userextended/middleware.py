# -*- coding: UTF-8 -*-

from django.contrib.auth import get_user
from django.http import HttpResponse
from django.shortcuts import render_to_response

from models import Pupil, Teacher, Staff

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            user = get_user(request);
            userprofile = user
            user.prefix = ''
            if user.is_authenticated():
                try:
                    if Pupil.objects.filter(user_ptr = user): 
                        userprofile = Pupil.objects.get(user_ptr=user)
                        userprofile.prefix = 'p'
                    elif Teacher.objects.filter(user_ptr = user): 
                        userprofile = Teacher.objects.get(user_ptr=user)
                        userprofile.prefix = 't'
                    elif Staff.objects.filter(user_ptr = user):
                        userprofile = Staff.objects.get(user_ptr = user)
                        userprofile.prefix = 's'
                    elif user.is_superuser: 
                        userprofile = user
                        userprofile.prefix = 'a'
                        userprofile.is_administrator = lambda: userprofile.is_superuser
                except:
                    userprofile = user
                    userprofile.prefix = ''
            else:
                userprofile = user
                userprofile.prefix = ''
            request._cached_user = userprofile
        return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()
        if request.user.is_authenticated():
            if request.user.prefix == 't':
                request.__class__.user_type = 'teacher'
                request.__class__.is_teacher = True
                request.__class__.is_pupil = False
            else:
                request.__class__.user_type = 'pupil'
                request.__class__.is_teacher = False
                request.__class__.is_pupil = True
        return None
