from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


# Register your models here.


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass


@admin.register(Passes)
class PassesAdmin(admin.ModelAdmin):
    pass
