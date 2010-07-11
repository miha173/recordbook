# -*- coding: UTF-8 -*-

from django.contrib import admin

from models import Book, Arrearage

class BookAdmin(admin.ModelAdmin):
    list_display = ('school', 'name', 'author')
    fields = ('school', 'name', 'author')
    
class ArreageAdmin(admin.ModelAdmin):
    list_display = ('pupil', 'book', 'take', 'owe_back', 'back')
    fields = ('pupil', 'book', 'owe_back')

admin.site.register(Book, BookAdmin)
admin.site.register(Arrearage, ArreageAdmin)