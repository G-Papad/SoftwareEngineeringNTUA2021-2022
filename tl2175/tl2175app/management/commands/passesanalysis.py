from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--op1', type=str, help="Visited Station's Operator ID")
        parser.add_argument('--op2', type=str, help="Visitor's Operator ID")
        parser.add_argument('--datefrom', type=str, default = "20200101", help="Date From")
        parser.add_argument('--dateto', type=str, default = "20210101", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)

    def handle(self, *args, **options):
        op1_ID = options['op1']
        op2_ID = options['op2']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']

        provider1 = Provider.objects.filter(providerAbbr=op1_ID)
        provider2 = Provider.objects.filter(providerAbbr=op2_ID)
        if (not provider1.exists()) or (not provider2.exists()):
            print("Invalid arguments: Provider does not exist")
            return
        if(df > dt):
            print("Invlide arguments: date_from > date_to")
            return

        try:
            dt = datetime.strptime(dt+"000000", "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            df = datetime.strptime(df+"000000", "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            print("Wrong DateTime Format")
            return

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
        try:
            info["NumberOfPasses"] = passes.count()
        except:
            info["NumberOfPasses"] = 0

        info["PassesList"] = []
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
            # toCSV = info['PassesList']
            # with open('passesanalysis', 'w', encoding = 'utf8', newline='') as output_file:
            #     fc = csv.DictWriter(output_file, field=toCSV[1].keys())
            #     fc.writeheader()
            #     fc.writerows(toCSV)
            print("FIX_CSV_FORMAT")
