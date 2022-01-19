from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--op1', type=str, help="Visited Station's Operator ID")
        parser.add_argument('--datefrom', type=str, default = "20050101", help="Date From")
        parser.add_argument('--dateto', type=str, default = "20210101", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)

    def handle(self, *args, **options):
        op1 = options['op1']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']

        provider1 = Provider.objects.filter(providerAbbr=op1)
        if (not provider1.exists()):
            print("Invalid arguments: Provider does not exist")
            return
        if(df > dt):
            print("Invlide arguments: date_from > date_to")
            return
        name_from = df
        name_to = dt
        try:
            dt = datetime.strptime(dt+"000000", "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            df = datetime.strptime(df+"000000", "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            print("Wrong DateTime Format")
            return
        response = {}
        response["op1ID"] = op1
        response["RequestTimeStamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        response["PeriodFrom"] = df
        response["PeriodTo"] = dt
        response["PPOList"] = []
        for provider in Provider.objects.all():
            op2 = provider.providerAbbr
            if op2 == op1:
                continue
            passes = Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1).filter(passes_fk2__vehicle_fk1__providerAbbr=op2).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
            try:
                pcount = passes.count()
                psum = passes.aggregate(Sum('charge'))["charge__sum"]
            except:
                #psum = 0
                pcount = 0
            if (psum == None):
                psum = 0
            dict = {"VisitingOperator": op2, "NumberOfPasses": pcount, "PassesCost": psum}
            response["PPOList"].append(dict)

        if format == 'json':
            print(response)
        else:
            name = "tl2175app/management/commands/results/ChargesBy_" + op1 + "_"  + name_from + "_" + name_to + ".csv"
            keys = response["PPOList"][0].keys()
            a_file = open(name, "w", newline='')
            dict_writer=csv.DictWriter(a_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(response["PPOList"])
            a_file.close()
