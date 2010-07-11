# -*- coding: utf-8 -*-

from datetime import date, timedelta
import pytils

from src.attendance.models import UsalTimetable

class TimetableDay:
    def __init__(self, grade, group, workday):
        workday = int(workday)
        self.day_n = workday
        self.day_ru = self.numDay2ruday(workday)
        self.grade = grade
        self.group = group
        self.today = False
        self.lessons = [lesson for lesson in UsalTimetable.objects.filter(grade = grade, group = group, workday = workday)]
        today = date.today().isoweekday()
        if today == workday:
            self.date = u'Сегодня'
            self.today = True
        elif today == workday -1:
            self.date = u'Завтра'
        elif today == workday + 1:
            self.date = u'Вчера'
        else:
            self.date = pytils.dt.ru_strftime(u"%d %B", inflected=True, date=date.today() + timedelta(days = (workday - today)))
            
    
    def numDay2ruday(self, workday):
        days = {1: u'Понедельник', 
                2: u'Вторник', 
                3: u'Среда', 
                4: u'Четверг', 
                5: u'Пятница', 
                6: u'Суббота', 
                7: u'Воскресенье', 
                }
        return days[int(workday)]