from django.contrib import admin
from .models import Rooms, Topics, Message

# Register your models here.

admin.site.register(Rooms)
admin.site.register(Topics)
admin.site.register(Message)
