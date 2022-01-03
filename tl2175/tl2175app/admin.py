from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


# Register your models here.


@admin.register(Provider, Station, Vehicle, Passes)
class StationAdmin(ImportExportModelAdmin):
    #list_display = ('stationid', 'stationProvider', 'stationName')
    pass

