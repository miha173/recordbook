# -*- coding: utf-8 -*-

import os

from django.template import TemplateDoesNotExist
from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

class PlaningError(Exception):
    pass

def load_template_from_app(template_name, template_dirs = None):
    if template_name[0] != '~': raise TemplateDoesNotExist, template_name
    
    template_name  = template_name[1:].split('/')
    
    if template_name[0] in settings.INSTALLED_APPS:
        app = settings.INSTALLED_APPS[settings.INSTALLED_APPS.index(template_name[0])]
    elif 'odaybook.' + template_name[0] in settings.INSTALLED_APPS:
        app = settings.INSTALLED_APPS[settings.INSTALLED_APPS.index('odaybook.' + template_name[0])]
    else:
        raise TemplateDoesNotExist, template_name

    try:
        mod = import_module(app)
    except ImportError, e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    
    filepath = os.path.join(template_dir, '/'.join(template_name[1:]))
    try:
        return open(filepath).read().decode(settings.FILE_CHARSET), filepath
    except IOError:
        raise TemplateDoesNotExist, template_name
    

load_template_from_app.is_usable = True