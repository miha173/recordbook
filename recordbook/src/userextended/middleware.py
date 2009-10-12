# -*- coding: UTF-8 -*-

from django.contrib.auth import get_user
from django.http import HttpResponse
from django.shortcuts import render_to_response

from models import Pupil, Teacher

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            user = get_user(request);
            if user.is_authenticated():
                try:
                    if user.username[0] == 'p':
                        userprofile = Pupil.objects.get(user_ptr=user)
                    elif user.username[0] == 't':
                        userprofile = Teacher.objects.get(user_ptr=user)
                except:
                    userprofile = user
            else:
                userprofile = user
            request._cached_user = userprofile
        return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()
        if request.user.is_authenticated():
            if request.user.username[0] == 't':
                request.__class__.user_type = 'teacher'
                request.__class__.is_teacher = True
                request.__class__.is_pupil = False
            else:
                request.__class__.user_type = 'pupil'
                request.__class__.is_teacher = False
                request.__class__.is_pupil = True
        return None
