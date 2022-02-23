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
        parser.add_argument('--datefrom', type=str, default = "20050101", help="Date From")
        parser.add_argument('--dateto', type=str, default = "20210101", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)
        parser.add_argument('--savejson', type=str, choices=['yes', 'no'], default = 'no', help='Would you like to write JSON data to a file?')

    def handle(self, *args, **options):
        op1 = options['op1']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']
        savejson = options['savejson']

        provider1 = Provider.objects.filter(providerAbbr=op1)

        if (not provider1.exists()):
            print("Invalid arguments: Provider does not exist", file = self.stdout)
            return
        
        if(df > dt):
            print("Invalid arguments: date_from > date_to", file = self.stdout)
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

        url = 'http://127.0.0.1:8000/interoperability/api/ChargesBy/' + op1 + '/' + name_from + '/' + name_to
        response = requests.get(url).json()

        if format == 'json':
            print(response, file = self.stdout)
            name1 = "tl2175app/management/commands/results/json/ChargesBy_" + op1 + "_" + name_from + "_" + name_to + ".json"
            if savejson == 'yes':
                with open(name1, 'w') as f:
                    json.dump(response, f)

        else:
            name = "tl2175app/management/commands/results/csv/ChargesBy_" + op1 + "_"  + name_from + "_" + name_to + ".csv"
            data_file = open(name, 'w', newline = '')
            data = response['PPOList']
            if data == []:
                keys = ['VisitingOperator', 'NumberOfPasses', 'PassesCost']
                csv_writer = csv.DictWriter(data_file, keys)
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
