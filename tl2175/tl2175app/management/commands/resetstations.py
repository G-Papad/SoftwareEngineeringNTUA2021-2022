from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime, date
from tl2175app.serializers import *
import csv, json
import requests

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--format', type=str, choices=['json', 'csv'], default = 'json', help='Data Format',)

    def handle(self, *args, **options):
        url = 'http://127.0.0.1:8000/interoperability/api/admin/resetstations'
        response = requests.post(url).json()
        if options['format'] == 'json':
            print(response)
        else:
            name = "tl2175app/management/commands/results/csv/resetstations-" + str(date.today()) + ".csv"
            data_file = open(name, 'w', newline = '')
            keys = response[0].keys()
            csv_writer = csv.DictWriter(data_file, keys)
            csv_writer.writeheader()
            count = 0
            for i in response:
                if count == 0:
                    csv_writer.writerow
                    count +=1
                csv_writer.writerow(i)
            data_file.close()
