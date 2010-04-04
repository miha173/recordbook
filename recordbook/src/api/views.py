# -*- coding: utf-8 -*-

import demjson
from hashlib import md5
from datetime import datetime, timedelta, date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.aggregates import Avg

import src
from src import settings
from src.userextended.models import School, Pupil, Teacher, Achievement
from src.library.models import Arrearage
from src.marks.models import Mark, ResultDate, Result
from src.attendance.models import UsalTimetable

from src.api import forms

def REST(request, model, id = 0):
    method = request.method
    
    models = settings.REST_MODELS
    Model = eval(settings.REST_MODELS2APPS[model][0])
    Form = eval(settings.REST_MODELS2APPS[model][1])

    status = 200
    render = u''
    headers = {}
    
#    status = 401
#    headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
    logined = False
    import base64
    from django.contrib.auth import authenticate, login
    if request.META.has_key('HTTP_HTTP_AUTHORIZATION'):
        auth = request.META['HTTP_HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                try:
                    uname, passwd = base64.b64decode(auth[1]).split(':')
                except:
                    uname = passwd = ''
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active and user.is_superuser:
                        logined = True
                        login(request, user)
                        request.user = user
    if not logined:
        method = 'Auth'
    
    if method == 'GET':
        if id:
            model = get_object_or_404(Model, id = id)
            render = model.serialize(Model.serialize_fields)
        else:
            Model.objects.all()
            render = Model.objects.serialize(Model.serialize_fields)
    elif method == 'HEAD':
        if id:
            model = get_object_or_404(Model, id = id)
        else:
            model = Model.objects.all().order_by('-rest_modified')[0]
        headers['Modified'] = model.rest_modified.isoformat()
    elif method == 'POST':
        import demjson
        try:
            data = demjson.decode(request.raw_post_data)
        except:
            status = 406
            render = 'Wrong data'
            return HttpResponse(render, status = status)
        if id:
            model = get_object_or_404(Model, id = id)
        else:
            model = Model()
            status = 201
        form = Form(data, instance = model)
        if form.is_valid():
            form.save()
            if status == 201:
                headers['Location'] = model.get_absolute_uri()
        else:
            status = 406
            render = form.errors
    elif method == 'DELETE':
        if id:
            get_object_or_404(Model, id = id).delete()
        else:
            status = 406
    elif method == 'OPTIONS':
        headers['Allow'] = 'get, head, post, delete'.upper()
    elif method == 'Auth':
        status = 401
        headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
    else:
        status = 501
    
    response = HttpResponse(render, status = status)
    for header in headers.keys():
        response[header] = headers[header]

    return response


def formatModel(s):
    return s[0].upper() + s[1:].lower()
    
    
            

