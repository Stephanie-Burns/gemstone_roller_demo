
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . import models


@admin.register(models.Gemstone)
class GemstoneAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        '_icon',
        'value',
        'clarity',
        'color',
        'description',
        'dmg_row_value',
        'id',
        'created_by'
    )

    def _icon(self, obj):
        url = reverse("admin:treasure_gemstoneicon_change", args=[obj.icon.id])
        return format_html('<a href="{}"><img src="{}" width="32" height="32"/></a>'.format(url, obj.icon.image.url))


@admin.register(models.GemstoneIcon)
class GemstoneIconAdmin(admin.ModelAdmin):
    exclude = (
        'file_hash',
        'height',
        'width'
    )
    list_display = (
        'icon',
        'name',
        'id',
        'height',
        'width',
        'created_by'
    )

    def icon(self, obj):
        return format_html('<img src="{}" width="32" height="32"/>'.format(obj.image.url))


admin.site.register(models.GemstoneClarity)
