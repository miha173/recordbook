# -*- coding: UTF-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.cache import cache

from models import Novetly, Paper, PhotoAlbum, Document

def main(request):
   return render_to_response('info/page.html')
            