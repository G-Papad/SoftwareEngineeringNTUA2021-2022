from import_export import resources
from .models import Station


class StationResource(resources.ModelResource):
    class meta:
        model = Station
        # skip_unchanged = True
        # report_skipped = True
        # exclude = ('id',)
        # import_id_fields = ('stationid',
        #                     'stationProvider', 'stationName')
