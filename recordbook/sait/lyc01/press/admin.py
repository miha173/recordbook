# -*- coding: UTF-8 -*-

from django.contrib import admin
from lyc01.press.models import Novetly, Paper, PhotoAlbum, Document

class NovetlyAdmin(admin.ModelAdmin):
    list_display = ('title',)

class PaperAdmin(admin.ModelAdmin):
    list_display = ('title',)

class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('title',)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Novetly, NovetlyAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
admin.site.register(Document, DocumentAdmin)