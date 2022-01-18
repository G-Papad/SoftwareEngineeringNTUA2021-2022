from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--op1', type=str, help="Visited Station's Operator ID")
        parser.add_argument('--op2', type=str, help="Visitor's Operator ID")
        parser.add_argument('--datefrom', type=str, default = "2005-01-01T00:00:000", help="Date From")
        parser.add_argument('--dateto', type=str, default = "2021-01-01T00:00:000", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)

    def handle(self, *args, **options):
        op1_ID = options['op1']
        op2_ID = options['op2']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']

        passes = Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1_ID).filter(passes_fk2__vehicle_fk1__providerAbbr=op2_ID).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        serializer = PassesSerializer(passes, many=True)
        augmented_serializer_data = list(serializer.data)

        info = {}
        info["op1_ID"] = op1_ID
        info["op2_ID"] = op2_ID
        info["RequestTimeStamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        info["PeriodFrom"] = df
        info["PeriodTo"] = dt
        info["NumberOfPasses"] = passes.count()
        info["PassesList"] = []
        #augmented_serializer_data.insert(0, info)
        index = 0
        for data in serializer.data:
            index += 1
            data["PassIndex"] = index
            data.pop("pass_type")
            if format=='json':
                info["PassesList"].append(data)

        if format == 'json':
            print(info)
        else:
            print ("FIX_FOR_CSV")
