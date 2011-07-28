# -*- coding: UTF-8 -*-
'''
    Context proccesor's для всей системы
'''
from datetime import date

from odaybook.userextended.models import Option

def plural(request):
    '''
        Значения для pytils
    '''
    result = {}
    result['page_plural'] = (u"страница", u"страницы", u"страниц")
    result['pupil_plural'] = ("ученик", "ученика", "учеников")
    return result

def menu(request):
    '''
        Всяческие констаны для отображения меню
    '''
    dirs = request.path.split('/')

    CM = ''
    if len(dirs)>1:
        CM = dirs[1]
    if len(dirs)>3:
        if dirs[2] == 'uni':
            CM = dirs[3]

    SM = ''
    if len(dirs)>2:
        SM = dirs[2]

    return {
            'FA': request.path,
            'CM': CM,
            'SM': SM,
    }

def environment(request):
    '''
        Подгрузка раздичных переменных окружения
    '''
    render = {}
    user = request.user
    if request.user.is_authenticated():
        if request.user.type == 'Pupil':
            render['subjects'] = user.get_subjects()

        if user.type not in ['Pupil', 'Parent']:
            try:
                render['vnc_link'] = Option.objects.get(key = 'vnc_link')
            except Option.DoesNotExist:
                pass
    render['current_year'] = date.today().year
    return render


