from django.contrib import admin
from .models import MessageClass



class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'message', 'image']

admin.site.register(MessageClass, MessageAdmin)