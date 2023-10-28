from django.contrib import admin

from .models import ChatRoom, ChatMessage, CurrentlyDeletedMessages, CurrentlyEditedMessages

# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(CurrentlyDeletedMessages)
admin.site.register(CurrentlyEditedMessages)
