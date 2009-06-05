# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.cache import cache

from models import Page

def get(request, application, pageid):
    applications = ('info', 'council', 'teacherroom', 'pride', 'science')
    if application in applications:
        page = Page.objects.get(id=int(pageid))
        return render_to_response('info/page.html', {'title': page.title, 'text': page.text})
        