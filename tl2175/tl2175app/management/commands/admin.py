from django.core.management.base import BaseCommand
from tl2175app.models import Vehicle, Passes, Station, Provider
from django.db.models import Sum
from datetime import datetime
from tl2175app.serializers import *
import csv, json
import io
import requests
from rest_framework.response import Response

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--passesupd', action='store_true', default=False, help="Add new passes")
        parser.add_argument('--source', type=str, default="null", help="Location of csv file")

    def handle(self, *args, **options):
        passesupd = options['passesupd']
        csv_file = open(options['source'])
        if passesupd:
            csvreader = csv.reader(csv_file)
            header = []
            header = next(csvreader)
            for row in csvreader:
                if row[0] == None:
                    break
                value = Passes()
                data = row[0].split(';')
                value.passid = data[0]
                value.timestamp = datetime.strptime(
                    data[1], "%d/%m/%Y %H:%M")
                value.charge = data[4]
                value.passes_fk1 = Station.objects.get(stationid=data[2])
                value.passes_fk2 = Vehicle.objects.get(vehicleid=data[3])
                try:
                    value.full_clean()
                except ValidationError:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                value.save()
            return Response([{"status": "OK"}])
