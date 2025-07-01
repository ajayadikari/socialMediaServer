from django.contrib import admin
from .models import ClubClass


class ClubAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(ClubClass, ClubAdmin)