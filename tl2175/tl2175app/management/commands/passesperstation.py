from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv, json

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



        passes = Passes.objects.filter(passes_fk1__stationid=pk).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        if not passes.exists():
            passes = []
        serializer = PassesSerializer(passes, many=True)

        header = {}
        header["Station"] = pk
        header["StationOperator"] = station.stationProvider
        header["RequestTimeStamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        header["PeriodFrom"] = df
        header["PeriodTo"] = dt
        try:
            header["NumberOfPasses"] = passes.count()
        except:
            header["NumberOfPasses"] = 0

        header["PassesList"] = []
        index = 0
        for data in serializer.data:
            index += 1
            Vehicle = passes[index-1].passes_fk2
            Vehicle_tagProvider = Vehicle.tagProvider
            data["PassIndex"] = index
            data["TagProvider"] = Vehicle_tagProvider
            data.pop("stationRef")
            header["PassesList"].append(data)

        if format == 'json':
            print(header)
            name1 = "tl2175app/management/commands/results/json/PassesPerStation_" + pk + "_" + name_from + "_" + name_to + ".json"
            if savejson == 'yes':
                with open(name1, 'w') as f:
                    json.dump(header, f)
        else:
            name = "tl2175app/management/commands/results/json/PassesPerStation_" + pk + "_" + name_from + "_" + name_to + ".csv"
            a_file = open(name, "w", newline='')
            if header['PassesList']==[]:
                dict_writer=csv.DictWriter(a_file)
            else:
                keys = header["PassesList"][0].keys()
                dict_writer=csv.DictWriter(a_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(header["PassesList"])
            a_file.close()
