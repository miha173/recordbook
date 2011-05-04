# -*- coding: UTF-8 -*-

import datetime

from django.contrib.auth import get_user
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext

from models import Pupil, Teacher, Staff, School, Option, BaseUser, Clerk, Parent, Superviser, Notify

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            user = get_user(request);
            userprofile = user
            userprofile.type = 'Anonymous'
            if user.is_authenticated():
                try:
                    userprofile = Clerk.objects.get(user_ptr = user)

                    if not userprofile.current_role:
                        if userprofile.roles.all():
                            userprofile.current_role = userprofile.roles.all()[0]
                            userprofile.save()
                        else:
                            raise

                    userprofile = userprofile.get_current_role()
                    userprofile.last_login = datetime.datetime.now()
                    if userprofile.type == 'Teacher':
                        Notify.objects.filter(type = '2', user = userprofile).delete()
                    userprofile.save()
                except Clerk.DoesNotExist:
                    userprofile = user
            else:
                if School.objects.filter(private_domain = request.META['HTTP_HOST']):
                    userprofile.private_salute = School.objects.filter(private_domain = request.META['HTTP_HOST'])[0].private_salute
            request._cached_user = userprofile
        return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()
        return None
    def process_response(self, request, response):
        # FIXME
#        if request.user.is_authenticated():
#            if hasattr(request.user, 'type') and request.user.type == 'Parent' and not request.user.pupils.all():
#                messages.error(request, u'К вашему профилю не добавлено ни одного ребёнка.')
#                return render_to_response("message.html", context_instance = RequestContext(request))
        return response
