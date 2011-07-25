# -*- coding: utf-8 -*-

import datetime

def get_fillability(lessons):
    '''
        Заполняемость дневников в относительных и абсолютных величинах.

        Ключи:
         * all
         * filled
         * not_filed_from_10_to_15_days
         * not_filed_more_15_days

        Каждому ключу, соответствует ключ с суффикосм _percent, содержащий относителбную величину.
       '''

    result = {}

    result['all'] = a = float(lessons.count())
    result['all_percent'] = 100
    if a == 0:
        result = {
            'all': 0, 'all_percent': 0,
            'filled': 0, 'filled_percent': 0,
            'not_filled_from_10_to_15_days': 0, 'not_filled_from_10_to_15_days_percent': 0,
            'not_filled_more_15_days': 0, 'not_filled_more_15_days_percent': 0,
        }
    else:
        result['filled'] = lessons.filter(fullness = True).count()
        result['filled_percent'] = 100*result['filled']/a
        result['not_filled_from_10_to_15_days'] = lessons.filter(fullness = False, date__range = (
                                                                        datetime.date.today() - datetime.timedelta(days = 15),
                                                                        datetime.date.today() - datetime.timedelta(days = 10))
                                                  ).count()
        result['not_filled_from_10_to_15_days_percent'] = 100*result['not_filled_from_10_to_15_days']/a
        result['not_filled_more_15_days'] = lessons.filter(fullness = False, date__lte = datetime.date.today() - datetime.timedelta(days = 15)).count()
        result['not_filled_more_15_days_percent'] = 100*result['not_filled_more_15_days']/a

    return result