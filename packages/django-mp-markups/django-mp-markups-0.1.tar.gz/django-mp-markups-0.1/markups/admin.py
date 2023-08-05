
from django.contrib import admin

from markups.models import Markup


@admin.register(Markup)
class MarkupAdmin(admin.ModelAdmin):

    list_display = ['value', 'category', 'manufacturer']
