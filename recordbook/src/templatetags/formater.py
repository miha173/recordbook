# *-* coding: utf-8 *-*

from django import template

register = template.Library()

@register.filter(name='number_format')
def number(value):
    value = unicode(value)
    i = value
    if value.find('.')!=-1:
        i = value[:value.find('.')]
        f = value[value.find('.')+1:]
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
