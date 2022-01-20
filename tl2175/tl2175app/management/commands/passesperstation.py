from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv, json
import requests

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--station', type=str, help="Passthrough Station ID")
        parser.add_argument('--datefrom', type=str, default = "20050101", help="Date From")
        parser.add_argument('--dateto', type=str, default = "20210101", help='Date To')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format')
        parser.add_argument('--savejson', type=str, choices=['yes', 'no'], default = 'no', help='Would you like to write JSON data to a file?')

    def handle(self, *args, **options):
        pk = options['station']
        df = options['datefrom']
        dt = options['dateto']
        format = options['format']
        savejson = options['savejson']

        station=Station.objects.filter(stationid=pk)
        if not station.exists():
            print("Invalid arguments: Station does not exist")
            return
        if(df>dt):
            print("Invalid arguments: date_from > date_to")
            return

        station=station[0]
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


        url = 'http://127.0.0.1:8000/interoperability/api/PassesPerStation/' + pk + '/'  + name_from + '/' + name_to
        header = requests.get(url).json()

        if format == 'json':
            print(header)
            name1 = "tl2175app/management/commands/results/json/PassesPerStation_" + pk + "_" + name_from + "_" + name_to + ".json"
            if savejson == 'yes':
                with open(name1, 'w') as f:
                    json.dump(header, f)
        else:
            name = "tl2175app/management/commands/results/csv/PassesPerStation_" + pk + "_" + name_from + "_" + name_to + ".csv"
            data_file = open(name, "w", newline='')
            data = header['PassesList']
            if data==[]:
                keys = ['passid', 'timestamp', 'charge', 'vehicleRef', 'pass_type', 'PassIndex', 'TagProvider']
                csv_writer=csv.DictWriter(data_file, keys)
            else:
                keys = data[0].keys()
                csv_writer=csv.DictWriter(data_file, keys)
            csv_writer.writeheader()
            count = 0
            for i in data:
                if count == 0:
                    csv_writer.writerow
                    count += 1
                csv_writer.writerow(i)
            data_file.close()
