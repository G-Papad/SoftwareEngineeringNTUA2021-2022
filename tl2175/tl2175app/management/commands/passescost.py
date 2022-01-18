from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--op1', type=str, help="Visited Station's Operator ID")
        parser.add_argument('--op2', type=str, help="Visitor's Operator ID")
        parser.add_argument('--datefrom', type=str, default = "2005-01-01 00:00:000[:00[.000000]][TZ]", help="Date From")
        parser.add_argument('--dateto', type=str, default = "2021-01-01 00:00:000[:00[.000000]][TZ]", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)

    def handle(self, *args, **options):
        op1 = options['op1']
        op2 = options['op2']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']

        provider1 = Provider.objects.filter(providerAbbr=op1)
        provider2 = Provider.objects.filter(providerAbbr=op2)
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

        passes = Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1).filter(passes_fk2__vehicle_fk1__providerAbbr=op2).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        provider = Provider.objects.filter(providerAbbr=op1)
        data = {}
        data["Operator1"] = op1
        data["Operator2"] = op2
        data["RequestTimestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["PeriodFrom"] = df
        data["PeriodTo"] = dt
        try:
            data["NumberOfPasses"] = passes.count()
            data["PassesCost"] = passes.aggregate(Sum('charge'))["charge__sum"]

        except:
            data["NumberOfPasses"] = 0
            data["PassesCost"] = 0
        print(data)
