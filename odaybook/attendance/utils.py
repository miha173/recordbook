# -*- coding: utf-8 -*-

from datetime import date, timedelta
import pytils

from odaybook.attendance.models import UsalTimetable

class TimetableDay(object):
    u'''
        Класс для удобного представления расписания дня.

        Использовать только потомки.
    '''
    def __init__(self, workday, day_date = None):
        workday = int(workday)
        self.day_n = workday
        self.day_ru = self.numDay2ruday(workday)
        today = date.today().isoweekday()
        if today == workday:
            self.date = u'Сегодня'
            self.today = True
        elif today == workday - 1:
            self.date = u'Завтра'
        elif today == workday + 1:
            self.date = u'Вчера'
        else:
            if date:
                self.date = pytils.dt.ru_strftime(u"%d %B", inflected=True, date=day_date)
            else:
                self.date = pytils.dt.ru_strftime(u"%d %B", inflected=True, date=date.today() + timedelta(days = (workday - today)))
        self.timestamp = (date.today() + timedelta(days = (workday - today))).isoformat()
        self.rings = {}


    def numDay2ruday(self, workday):
        u'''Руссификация'''
        days = {1: u'Понедельник',
                2: u'Вторник',
                3: u'Среда',
                4: u'Четверг',
                5: u'Пятница',
                6: u'Суббота',
                7: u'Воскресенье',
                }
        return days[int(workday)]

class TimetableDayPupil(TimetableDay):
    u'''
        Расписание дня ученика.
    '''
    def __init__(self, workday, pupil, *args, **kwargs):
        from odaybook.userextended.models import PupilConnection
        super(TimetableDayPupil, self).__init__(workday, *args, **kwargs)
        self.pupil = pupil
        self.lessons = {}
        for lesson in UsalTimetable.objects.filter(grade = pupil.grade, workday = workday):
            try:
                connection = pupil.pupilconnection_set.all().filter(subject = lesson.subject)[0]
            except IndexError:
                connection = PupilConnection(value = '0')
            if connection.value == '0' or connection.value == lesson.group:
                self.lessons[int(lesson.number)] = lesson

class TimetableDayGrade(TimetableDay):
    u'''
        Расписание на день для класса. 
    '''
    def __init__(self, workday, grade, *args, **kwargs):
        super(TimetableDayGrade, self).__init__(workday, *args, **kwargs)
        self.grade = grade
        self.lessons = {}
        for lesson in xrange(10): self.lessons[lesson+1] = []
        for lesson in UsalTimetable.objects.filter(grade = grade, workday = workday):
            self.lessons[int(lesson.number)].append(lesson)
