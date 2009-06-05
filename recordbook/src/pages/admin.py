# -*- coding: UTF-8 -*-

from django.contrib import admin
from src.pages.models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Page, PageAdmin);