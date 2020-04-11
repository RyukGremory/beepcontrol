from django.contrib import admin
from .models import Institutions,Campus,Building,Locks,Rooms

# Register your models here.
admin.site.register(Institutions)
admin.site.register(Campus)
admin.site.register(Building)
admin.site.register(Locks)
admin.site.register(Rooms)