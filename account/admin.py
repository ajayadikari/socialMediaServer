from django.contrib import admin
from .models import User


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff']

admin.site.register(User, AccountAdmin)