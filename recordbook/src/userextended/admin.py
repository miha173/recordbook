# -*- coding: UTF-8 -*-

from django.contrib import admin
from src.userextended.models import Grade, Subject, Teacher, Pupil

class GradeAdmin(admin.ModelAdmin):
    list_display = ('long_name',)
    ordering = ('long_name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TeacherAdmin(admin.ModelAdmin):
    def fio(obj):
        return obj.last_name+' '+obj.first_name+' '+obj.middle_name
    fio.short_description = u'Фамилия, имя, отчество'
    list_display = (fio, 'grade')
    fieldsets = [
                 (u'Общая информация', {'fields': ['last_name', 'first_name', 'middle_name', 'grade']}),
                 (u'Преподавание', {'fields': ['grades', 'subjects']})
                ]
    search_fields = ['first_name', 'last_name']
    ordering = ('last_name',)

class PupilAdmin(admin.ModelAdmin):
    def fio(obj):
        return obj.last_name+' '+obj.first_name+' '+obj.middle_name
    fio.short_description = u'Фамилия, имя, отчество'
    list_display = (fio,)
    fields = ('last_name', 'first_name', 'middle_name', 'grade')
    search_fields = ['first_name', 'last_name']
    ordering = ('last_name',)
    
admin.site.register(Grade, GradeAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Pupil, PupilAdmin)
admin.site.register(Teacher, TeacherAdmin)