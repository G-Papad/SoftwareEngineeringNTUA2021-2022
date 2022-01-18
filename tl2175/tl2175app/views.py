import io
from django.shortcuts import render
from .models import Vehicle, Passes, Station, Provider
#from django.forms import MemberForm
from .resources import StationResource
from django.contrib import messages
from tablib import Dataset, Databook
from django.http import HttpResponse, JsonResponse, HttpRequest
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from django.http import Http404
from rest_framework.views import APIView
from datetime import datetime
from django.db.models import Sum
from django.db import connection
from django.db.utils import OperationalError
import csv
from datetime import datetime
from django.core.exceptions import ValidationError, BadRequest


def upload_from_xslx(request):
    if request.method == 'POST':
        # station_resource = StationResource()
        dataset = Databook()
        new_station = request.FILES['myfile']

        if not new_station.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_station.read(), format='xlsx')
        for datasheet in imported_data.sheets():
            print(datasheet.title)
            if datasheet.title == 'providers':
                for data in datasheet:
                    if data[0] == None:
                        break
                    value = Provider()
                    value.providerAbbr = data[0]
                    value.providerName = data[1]
                    value.iban = data[2]
                    value.bankname = data[3]
                    value.save()
            elif datasheet.title == 'stations':
                for data in datasheet:
                    if data[0] == None:
                        break
                    value = Station()
                    value.stationid = data[0]
                    #value.stationProvider = data[1]
                    value.stationName = data[2]
                    value.station_fk = Provider.objects.get(
                        providerName=data[1])
                    value.save()
            elif datasheet.title == 'vehicles_100':

                for data in datasheet:
                    if data[0] == None:
                        break
                    value = Vehicle()
                    value.vehicleid = data[0]
                    value.tagid = data[1]
                    value.licenceYear = data[4]
                    #value.tagProvider = data[2]
                    #value.tagProviderAbbr = data[3]
                    value.vehicle_fk1 = Provider.objects.get(
                        providerName=data[2])
                    value.save()
            elif datasheet.title == 'passes100_8000':
                for data in datasheet:
                    if data[0] == None:
                        break
                    value = Passes()
                    value.passid = data[0]
                    value.timestamp = data[1]
                    value.charge = data[4]
                    #value.stationRef = data[2]
                    #value.vehicleRef = data[3]
                    value.passes_fk1 = Station.objects.get(stationid=data[2])
                    value.passes_fk2 = Vehicle.objects.get(vehicleid=data[3])
                    value.save()

    return render(request, 'upload.html')


def index(request):
    vehicles = Vehicle.objects.all()
    passes = Passes.objects.all()
    stations = Station.objects.all()
    providers = Provider.objects.all()

    return render(request, 'index.html', {
        'vehicles': vehicles,
        'passes': passes,
        'stations': stations,
        'providers': providers})


class PassesPerStation(APIView):
    def get_object(self, pk, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__stationid=pk).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except Passes.DoesNotExist:
            raise BadRequest("Invalid Request")

    def get(self, request, pk, df, dt):
        try:
            dt = datetime.strptime(dt, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            df = datetime.strptime(df, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            raise BadRequest("Wrong DateTime Format")
        try:
            format = request.GET['format']
        except:
            format = 'json'
        passes = self.get_object(pk, df, dt)
        serializer = PassesSerializer(passes, many=True)
        header = {}
        header["Station"] = pk
        try:
            station = passes[0].passes_fk1
        except:
            raise BadRequest("Invalid Request")
        header["StationOperator"] = station.stationProvider
        header["RequestTimeStamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        header["PeriodFrom"] = df
        header["PeriodTo"] = dt
        header["NumberOfPasses"] = passes.count()
        header["PassesList"] = []
        #augmented_serializer_data = list(serializer.data)
        #augmented_serializer_data.insert(0, header)
        index = 0
        for data in serializer.data:
            index += 1
            Vehicle = passes[index-1].passes_fk2
            Vehicle_tagProvider = Vehicle.tagProvider
            data["PassIndex"] = index
            data["TagProvider"] = Vehicle_tagProvider
            data.pop("stationRef")
            if format == 'json':
                header["PassesList"].append(data)

        if format == 'json':
            return Response(header)
        return Response(serializer.data)


class PassesAnalysis(APIView):
    def get_object(self, op1_ID, op2_ID, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1_ID).filter(passes_fk2__vehicle_fk1__providerAbbr=op2_ID).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except Passes.DoesNotExist:
            raise BadRequest("Invalid Request")

    def get(self, request, op1_ID, op2_ID, df, dt):
        try:
            dt = datetime.strptime(dt, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            df = datetime.strptime(df, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            raise BadRequest("Wrong DateTime Format")
        try:
            format = request.GET['format']
        except:
            format = 'json'
        passes = self.get_object(op1_ID, op2_ID, df, dt)
        serializer = PassesSerializer(passes, many=True)
        augmented_serializer_data = list(serializer.data)

        info = {}
        info["op1_ID"] = op1_ID
        info["op2_ID"] = op2_ID
        info["RequestTimeStamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        info["PeriodFrom"] = df
        info["PeriodTo"] = dt
        info["NumberOfPasses"] = passes.count()
        info["PassesList"] = []
        #augmented_serializer_data.insert(0, info)
        index = 0
        for data in serializer.data:
            index += 1
            data["PassIndex"] = index
            data.pop("pass_type")
            info["PassesList"].append(data)

        if (format == 'json'):
            return Response(info, content_type='json')
        return Response(info["PassesList"])


class PassesCost(APIView):
    def get_object(self, op1, op2, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1).filter(passes_fk2__vehicle_fk1__providerAbbr=op2).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except Passes.DoesNotExist:
            raise BadRequest("Invalid Request")

    def get(self, request, op1, op2, df, dt):
        try:
            dt = datetime.strptime(dt, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            df = datetime.strptime(df, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            raise BadRequest("Wrong DateTime Format")
        try:
            format = request.GET['format']
        except:
            format = 'json'
        passes = self.get_object(op1, op2, df, dt)
        provider = Provider.objects.filter(providerAbbr=op1)
        data = {}
        data["Operator1"] = op1
        data["Operator2"] = op2
        data["RequestTimestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["PeriodFrom"] = df
        data["PeriodTo"] = dt
        data["NumberOfPasses"] = passes.count()
        data["PassesCost"] = passes.aggregate(Sum('charge'))["charge__sum"]
        return Response(data)


class ChargesBy(APIView):
    def get_object(self, op1, op2, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1).filter(passes_fk2__vehicle_fk1__providerAbbr=op2).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except:
            raise BadRequest("Invalid Request")

    def get(self, request, op1, df, dt):
        try:
            dt = datetime.strptime(dt, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
            df = datetime.strptime(df, "%Y%m%d%H%M%S").strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            raise BadRequest("Wrong DateTime Format")
        try:
            format = request.GET['format']
        except:
            format = 'json'
        response = {"opID": op1, "RequestTimeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "PeriodFrom": df,
                    "PeriodTo": dt, "PPOList": []}
        for provider in Provider.objects.all():
            op2 = provider.providerAbbr
            if op2 == op1:
                continue
            passes = self.get_object(op1, op2, df, dt)
            dict = {"VisitingOperator": op2, "NumberOfPasses": passes.count(
            ), "PassesCost": passes.aggregate(Sum('charge'))["charge__sum"]}
            response["PPOList"].append(dict)
        if format == 'json':
            return Response(response)
        return Response(response["PPOList"])


class PassesUpdate(APIView):
    # def get(self, request, format=None):
    #     snippets = Passes.objects.all()
    #     serializer = PassesSerializerAll(snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        try:
            format = request.GET['format']
        except:
            format = 'json'
        if format == "json":
            for data in request.data:
                value = Passes()
                value.passid = data["passID"]
                value.timestamp = data["timestamp"]
                value.charge = data["charge"]
                value.passes_fk1 = Station.objects.get(
                    stationid=data["stationRef"])
                value.passes_fk2 = Vehicle.objects.get(
                    vehicleid=data["vehicleRef"])

                try:
                    value.full_clean()
                except ValidationError:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                value.save()
            return Response([{"status": "OK"}])

        if format == "csv":
            dataset = Dataset()
            csv_file = request.FILES['file']
            csvreader = csv.reader(io.StringIO(
                csv_file.read().decode('utf-8')), delimiter=';')
            header = next(csvreader)
            # imported_data = dataset.load(io.StringIO(
            #     csv_file.read().decode('utf-8')), 'csv')
            # print(imported_data)
            for data in csvreader:
                if data[0] == None:
                    break
                value = Passes()
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


class healthcheck(APIView):
    def get(self, request):
        try:
            connection.ensure_connection()
            return Response([{"status": "OK", "dbconnection": "connectionstring"}])
        except OperationalError:
            return Response([{"status": "failed"}])


class resetpasses(APIView):
    def post(self, request):
        try:
            for instance in Passes.objects.all().iterator():
                instance.delete()
            return Response([{"status": "OK"}])
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return Response([{"status": "failed", "error type": str(err)}])
        except:
            return Response([{"status": "failed"}])


class resetstations(APIView):
    def post(self, request):
        try:
            for instance in Station.objects.all().iterator():
                instance.delete()
            with open("tl2175app/starting_data/sampledata01_stations.csv", "r") as f:
                csvreader = csv.reader(f, delimiter=';')
                header = next(csvreader)
                for row in csvreader:
                    value = Station()
                    value.stationid = row[0]
                    value.stationName = row[2]
                    value.station_fk = Provider.objects.get(
                        providerName=row[1])
                    value.save()
            return Response([{"status": "OK"}])
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return Response([{"status": "failed", "error type": str(err)}])
        except:
            return Response([{"status": "failed"}])


class resetvehicles(APIView):
    def post(self, request):
        try:
            for instance in Vehicle.objects.all().iterator():
                instance.delete()
            with open("tl2175app/starting_data/sampledata01_vehicles_100.csv", "r") as f:
                csvreader = csv.reader(f, delimiter=';')
                header = next(csvreader)
                for row in csvreader:
                    value = Vehicle()
                    value.vehicleid = row[0]
                    value.tagid = row[1]
                    value.licenceYear = row[4]
                    value.vehicle_fk1 = Provider.objects.get(
                        providerName=row[2])
                    value.save()
            return Response([{"status": "OK"}])
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return Response([{"status": "failed", "error type": str(err)}])
        except:
            return Response([{"status": "failed"}])
