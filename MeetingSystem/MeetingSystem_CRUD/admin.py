from django.contrib import admin

# Register your models here.

from .models import Meeting, Event

admin.site.register(Meeting)
admin.site.register(Event)
