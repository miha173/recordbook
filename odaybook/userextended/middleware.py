# -*- coding: UTF-8 -*-

import datetime

from django.contrib.auth import get_user
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from django.template import RequestContext

from models import Pupil, Teacher, Staff, School, Option, BaseUser, Clerk, Parent, Superviser, Notify
import logging

logger = logging.getLogger(__name__)

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            logger.info(u'Начата загрузка view для пользователя')
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
                logger.info(u'Закончена загрузка middleware view для пользователя типа %s с id=%d' % (userprofile.type, userprofile.id))
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
        if hasattr(request, 'user') and request.META['PATH_INFO']!='/curatorship/send-append-request/' and request.user.is_authenticated():
            if hasattr(request.user, 'type') and request.user.type == 'Parent':
                if request.user.pupils.all():
                    if request.user.current_pupil:
                        request.user.current_pupil = request.user.pupils.all()[0]
                        request.user.save()
                    else:
                        messages.error(request, u'К вашему профилю не добавлено ни одного ребёнка. <a href="/curatorship/send-append-request">Отправить запрос на прикрепление ребёнка.</a>')
                        return render_to_response("message.html", context_instance = RequestContext(request))

        return response
    
class AdminPeepingMiddleware(object):
    def process_request(self, request):
        from django.http import HttpResponseRedirect, HttpResponse, Http404
        if int(request.COOKIES.get('zombie', False)):
            if not request.user.type != 'SuperUser': raise Http404('not superuser')
            user = request.COOKIES.get('zombie')
            user = get_object_or_404(Clerk, id = user)
            if not user.current_role: user.current_role = user.roles.all()[0]
            request.user = user.get_current_role()