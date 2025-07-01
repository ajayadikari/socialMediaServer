from django.contrib import admin
from .models import ExperienceModel


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'company_name']

admin.site.register(ExperienceModel, ExperienceAdmin)