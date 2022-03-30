from django.contrib import admin
from .models import Chat, Message, Profile
# Register your models here.

class MessageAdmin(admin.ModelAdmin):    
    fields = ('chat', 'text','created_at', 'author', 'receiver')    
    list_display = ('created_at', 'author', 'text', 'receiver')    
    search_fields = ('text',)

admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
admin.site.register(Profile)
