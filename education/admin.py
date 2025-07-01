from django.contrib import admin
from .models import EducationModel



class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution_name', 'major', 'degree']

admin.site.register(EducationModel, EducationAdmin)