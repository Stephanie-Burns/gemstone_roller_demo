
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Gemstone, GemstoneIcon


@admin.register(Gemstone)
class GemstoneAdmin(admin.ModelAdmin):
    list_display = ('name', '_icon', 'id', 'description', 'value',)
    def _icon(self, obj):
        url = reverse("admin:treasure_gemstoneicon_change", args=[obj.icon.id])
        return format_html('<a href="{}"><img src="{}" width="32" height="32"/></a>'.format(url, obj.icon.image.url))

@admin.register(GemstoneIcon)
class GemstoneIconAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'id', 'width', 'height')

    def icon(self, obj):
        return format_html('<img src="{}" width="32" height="32"/>'.format(obj.image.url))
