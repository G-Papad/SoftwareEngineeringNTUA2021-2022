from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv, json
import requests

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--op1', type=str, help="Visited Station's Operator ID")
        parser.add_argument('--op2', type=str, help="Visitor's Operator ID")
        parser.add_argument('--datefrom', type=str, default = "20050101", help="Date From")
        parser.add_argument('--dateto', type=str, default = "20210101", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)
        parser.add_argument('--savejson', type=str, choices=['yes', 'no'], default = 'no', help='Would you like to write JSON data to a file?')

    def handle(self, *args, **options):
        op1 = options['op1']
        op2 = options['op2']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']
        savejson = options['savejson']

        provider1 = Provider.objects.filter(providerAbbr=op1)
        provider2 = Provider.objects.filter(providerAbbr=op2)
        if (not provider1.exists()) or (not provider2.exists()):
            print("Invalid arguments: Provider does not exist", file=self.stdout)
            return
        if(df > dt):
            print("Invlide arguments: date_from > date_to", file=self.stdout)
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

        passes = Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1).filter(passes_fk2__vehicle_fk1__providerAbbr=op2).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        provider = Provider.objects.filter(providerAbbr=op1)

        url = 'http://127.0.0.1:8000/interoperability/api/PassesCost/' + op1 + '/' + op2 + '/' + name_from + '/' + name_to
        response = requests.get(url).json()
        if format == 'json':
            print(response, file=self.stdout)
            name1 = "tl2175app/management/commands/results/json/PassesCost" + op1 + "_"  + op2 + '_' + name_from + "_" + name_to + ".json"
            if savejson == 'yes':
                with open(name1, 'w') as f:
                    json.dump(response, f)
        else:
            name = "tl2175app/management/commands/results/csv/PassesCost" + op1 + "_" + op2 + '_' + name_from + "_" + name_to + ".csv"
            data_file = open(name, 'w', newline = '')
            data = response
            if data == []:
                keys = ['Operator1', 'Operator2', 'RequestTimestamp', 'PeriodFrom', 'PeriodTo', 'NumberOfPasses', 'PassesCost']
                csv_writer = csv.DictWriter(data_file, keys)
            else:
                keys = data.keys()
                print(keys, file=self.stdout)
                csv_writer = csv.DictWriter(data_file, keys)
            csv_writer.writeheader()
            csv_writer.writerow(data)
            data_file.close()
