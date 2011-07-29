# -*- coding: utf-8 -*-
'''
    Фильтры, необходимые для красивой отрисовки формы ввода оценок
'''

from django import template

register = template.Library()

@register.filter
def next_date(current, array):
    '''
        Следующая дата из списка
    '''
    new_index = array.index(current) + 1
    if new_index >= len(array):
        return None
    else:
        return array[new_index].id

@register.filter
def prev_date(current, array):
    '''
        Предыдущая дата из списка
    '''
    new_index = array.index(current) - 1
    if new_index < 0:
        return None
    else:
        return array[new_index].id

@register.filter
def up_pupil(current, array):
    '''
        Предыдущий ученик из списка.
    '''
    array = list(array)
    new_index = array.index(current) - 1
    if new_index < 0:
        return None
    else:
        return array[new_index].id

@register.filter
def first_pupil(current, array):
    '''
        Первый ученик из списка.
    '''
    return list(array)[0].id

@register.filter
def down_pupil(current, array):
    '''
        Следующий ученик из списка.
    '''
    array = list(array)
    new_index = array.index(current) + 1
    if new_index >= len(array):
        return None
    else:
        return array[new_index].id

@register.filter
def get_mark(pupil, lesson):
    '''
        Вывод оценки данного ученика за данное занятие.
    '''
    from odaybook.marks.models import Mark
    from django.utils.safestring import mark_safe
    if Mark.objects.filter(lesson = lesson, pupil = pupil):
        mark = Mark.objects.filter(lesson = lesson, pupil = pupil)[0]
        return mark_safe('<div class="mark-%s">%s</div>' % (mark.get_type(), str(mark)))
    else:
        return ''
