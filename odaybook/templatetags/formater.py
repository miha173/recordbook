# -*- coding: utf-8 -*-

import urllib

from django import template

register = template.Library()

@register.filter(name='number_format')
def number(value, places = None):
    try:
        float(value)
    except ValueError:
        return value
    value = unicode(value)
    i = value
    if value.find('.')!=-1:
        i = value[:value.find('.')]
        f = value[value.find('.')+1:]
        if places:
            f = f[:int(places)]
    else:
        i = value
        f = 0
    i = i[::-1]
    str = ''
    for x in xrange(0, len(i), 3):
        str += i[x:x+3] + " "
    str = str[::-1].strip()
    if f:
        return str + "," + f
    else:
        return str

@register.filter
def urllibencode(value):
    return urllib.urlencode(value)
