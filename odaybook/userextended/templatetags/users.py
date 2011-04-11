# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def has_role(clerk, role):
    return clerk.has_role(role)
