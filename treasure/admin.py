
from django.contrib import admin
from django.utils.html import format_html
from .models import Gemstone, GemstoneIcon


@admin.register(Gemstone)
class GemstoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'value')


@admin.register(GemstoneIcon)
class GemstoneIconAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'id', 'width', 'height')

    def thumbnail(self, obj):
        return format_html('<img src="{}" width="32" height="32"/>'.format(obj.image.url))
