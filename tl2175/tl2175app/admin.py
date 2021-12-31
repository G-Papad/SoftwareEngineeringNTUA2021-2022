from django.contrib import admin
from .models import Provider, Station, Vehicle, Passes

# Register your models here.

admin.site.register(Provider)

admin.site.register(Station)

admin.site.register(Vehicle)

admin.site.register(Passes)
