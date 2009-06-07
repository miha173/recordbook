# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
#from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from models import Teacher
from forms import LoginForm
