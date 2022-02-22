from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv, json, os
import requests

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--op1', type=str, help="Visited Station's Operator ID", dest = 'op1',)
        parser.add_argument('--op2', type=str, help="Visitor's Operator ID",  dest = 'op2')
        parser.add_argument('--datefrom', type=str, default = "20050101", help="Date From")
        parser.add_argument('--dateto', type=str, default = "20210101", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)
        parser.add_argument('--savejson', type=str, choices=['yes', 'no'], default = 'no', help='Would you like to write JSON data to a file?')

    def handle(self, *args, **options):
        op1_ID = options['op1']
        op2_ID = options['op2']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']
        savejson = options['savejson']

        provider1 = Provider.objects.filter(providerAbbr=op1_ID)
        provider2 = Provider.objects.filter(providerAbbr=op2_ID)
        if (not provider1.exists()) or (not provider2.exists()):
            print("Invalid arguments: Provider does not exist", file = self.stdout)
            return
        if(df > dt):
            print("Invlide arguments: date_from > date_to", file = self.stdout)
            return
        name_from = df
        name_to = dt
        try:
            dt = datetime.strptime(dt+"000000", "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            df = datetime.strptime(df+"000000", "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            print("Wrong DateTime Format", file = self.stdout)
            return

        url = 'http://127.0.0.1:8000/interoperability/api/PassesAnalysis/' + op1_ID + '/' + op2_ID + '/' + name_from + '/' + name_to
        passes = requests.get(url).json()
#savedata
        if format == 'json':
            print(passes, file = self.stdout)
            name1 = "tl2175app/management/commands/results/json/PassesAnalysis_" + op1_ID + "_" + op2_ID + "_" + name_from + "_" + name_to + ".json"
            if savejson == 'yes':
                with open(name1, 'w') as f:
                    json.dump(passes, f)
        else:
            name = "tl2175app/management/commands/results/csv/PassesAnalysis_" + op1_ID + "_" + op2_ID + "_" + name_from + "_" + name_to + ".csv"
            data_file = open(name, 'w', newline = '')
            data = passes['PassesList']
            if data == []:
                keys = ['passid', 'timestamp', 'charge', 'stationRef', 'vehicleRef', 'PassIndex']
                csv_writer=csv.DictWriter(data_file, keys)
            else:
                keys = data[0].keys()
                csv_writer = csv.DictWriter(data_file, keys)
            csv_writer.writeheader()
            count = 0
            for i in data:
                if count == 0:
                    csv_writer.writerow
                    count +=1
                csv_writer.writerow(i)
            data_file.close()
