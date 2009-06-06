# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
#from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from models import Teacher
from forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            return HttpResponseRedirect('/')
        else:
            return render_to_response('userextended/login.html', {'form': form})
    else: 
        if not request.session.get('username'):
            return render_to_response('userextended/login.html',{'form': LoginForm()})
        else: 
            return HttpResponseRedirect('/')

def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/auth/login')