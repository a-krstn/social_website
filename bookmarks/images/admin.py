from django.contrib import admin
from .models import Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']
