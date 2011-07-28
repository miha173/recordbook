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

@register.tag
def main_menu_block(parser, token):
    args_names = ['name', 'link', 'color', 'bool_arg1', 'bool_arg2']
    args = token.split_contents()
    args = args[1:]

    kwargs = {}
    for arg in xrange(len(args_names)):
        kwargs[args_names[arg]] = args[arg]

    return MenuBlockNode(**kwargs)

class MenuBlockNode(template.Node):

    colors = ['blue', 'yellow', 'green', 'red', 'purple', 'gay']
    current_color = 0

    def __init__(self, **kwargs):
        self.keys = []
        for key, item in kwargs.items():
            self.keys.append(key)
            setattr(self, key, template.Variable(item))

    def render(self, context):
        for key in self.keys:
            setattr(self, key, getattr(self, key).resolve(context))

        if 'current_color' not in context:
            context['current_color'] = self.current_color

        if self.color == '':
            self.color = self.colors[context['current_color']]
            context['current_color'] += 1
        else:
            try:
                self.colors.remove(self.color)
            except ValueError: pass

        condition = self.bool_arg1 == self.bool_arg2
        if '/uni/userextended.School/' in self.link:
            condition = condition or context.get('school', False)

        if condition:
            return '<big class="%s">%s</big>' % (self.color, self.name)
        else:
            return '<a href="%s">%s</a>' % (self.link, self.name)

@register.simple_tag
def padding_menu_block(name, link, arg):
    '''
        {% if SM == "connections" %}<h1>Связки</h1> {% else %}<a href="/curatorship/connections/">Связки</a>{% endif %}
    '''
    if link.split('/')[2] == arg:
        return '<h1>%s</h1>' % name
    else:
        return '<a href="%s">%s</a>' % (link, name)