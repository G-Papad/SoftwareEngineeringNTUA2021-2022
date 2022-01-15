from django.shortcuts import render
from .models import Vehicle, Passes, Station, Provider
#from django.forms import MemberForm

# Create your views here.

from .resources import StationResource
from django.contrib import messages
from tablib import Dataset, Databook
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from datetime import datetime
from django.db.models import Sum
from django.db import connection
from django.db.utils import OperationalError
import csv


# def transportation(request):
#     if request.method == 'POST':
#         # form = MemberForm(request.POST or None)
#         operator1 = request.POST['operator1']
#         operator2 = request.POST['operator2']
#         datefrom = request.POST['datefrom']
#         dateto = request.POST['dateto']
#
#         posts = Passes.objects.raw("""
#             select pass.*
#             FROM
#             	providers prov
#             	passes pass
#             	vehicles veh
#             	station
#             where
#             	pass.timestamp BETWEEN datefrom and dateto
#             	AND pass.stationRef = station.providerName
#             	AND station.providerName = prov.providerName
#             	AND prov.providerName = operator1
#             	AND pass.vehicleRef = veh.vehicleid
#             	AND veh.tagProvider = operator2""")
#
#         return render(request, 'transportation.html', {'data': posts})
#     return render(request, 'transportation.html', {})


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


class Providers_list(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class Providers_Details(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


# class PassesPerStation(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Passes.objects.filter(passes_fk1__stationid=pk).exclude(
#         timestamp__gte=dt).filter(timestamp_gte=df)
#     serializer_class = PassesSerializer

#  Passes.objects.filter(charge='2.8').filter(stationRef='KO01')

class PassesPerStation(APIView):
    def get_object(self, pk, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__stationid=pk).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except Passes.DoesNotExist:
            raise Http404

    def get(self, request, pk, df, dt, format=None):
        passes = self.get_object(pk, df, dt)
        serializer = PassesSerializer(passes, many=True)
        header = {}
        header["Station"] = pk
        station = passes[0].passes_fk1
        header["StationOperator"] = station.stationProvider
        header["RequestTimeStamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        header["PeriodFrom"] = df
        header["PeriodTo"] = dt
        header["NumberOfPasses"] = passes.count()

        augmented_serializer_data = list(serializer.data)
        augmented_serializer_data.insert(0, header)
        index = 0
        for data in serializer.data:
            index += 1
            Vehicle = passes[index-1].passes_fk2
            Vehicle_tagProvider = Vehicle.tagProvider
            data["PassIndex"] = index
            data["TagProvider"] = Vehicle_tagProvider
            data.pop("stationRef")

        return Response(augmented_serializer_data)


class PassesAnalysis(APIView):
    def get_object(self, op1_ID, op2_ID, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1_ID).filter(passes_fk2__tagProviderAbbr=op2_ID).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except Passes.DoesNotExist:
            raise Http404

    def get(self, request, op1_ID, op2_ID, df, dt, format=None):
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
        augmented_serializer_data.insert(0, info)
        index = 0
        for data in serializer.data:
            index += 1
            data["PassIndex"] = index
            data.pop("pass_type")

        return Response(augmented_serializer_data)


class PassesCost(APIView):
    def get_object(self, op1, op2, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1).filter(passes_fk2__tagProviderAbbr=op2).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except Passes.DoesNotExist:
            raise Http404

    def get(self, request, op1, op2, df, dt, format=None):
        passes = self.get_object(op1, op2, df, dt)
        provider = Provider.objects.filter(providerAbbr=op1)
        # serializer = PassesSerializer(passes, many=True)
        serializer = ProviderSerializer(provider, many=True)
        for data in serializer.data:
            data["Operator1"] = op1
            data["Operator2"] = op2
            data["RequestTimestamp"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            data["PeriodFrom"] = df
            data["PeriodTo"] = dt
            data["NumberOfPasses"] = passes.count()
            data["PassesCost"] = passes.aggregate(Sum('charge'))["charge__sum"]
            data.pop("providerAbbr")
            data.pop("providerName")
            data.pop("iban")
            data.pop("bankname")
        return Response(serializer.data)


class ChargesBy(APIView):
    def get_object(self, op1, op2, df, dt):
        try:
            return Passes.objects.filter(passes_fk1__station_fk__providerAbbr=op1).filter(passes_fk2__tagProviderAbbr=op2).exclude(timestamp__gte=dt).filter(timestamp__gte=df)
        except Passes.DoesNotExist:
            raise Http404

    def get(self, request, op1, df, dt, format=None):
        response = [{"opID": op1, "RequestTimeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "PeriodFrom": df,
                     "PeriodTo": dt}]
        for provider in Provider.objects.all():
            op2 = provider.providerAbbr
            if op2 == op1:
                continue
            passes = self.get_object(op1, op2, df, dt)
            dict = {"VisitingOperator": op2, "NumberOfPasses": passes.count(
            ), "PassesCost": passes.aggregate(Sum('charge'))["charge__sum"]}
            response.append(dict)
        return Response(response)


class PassesUpdate(APIView):
    def get(self, request):
        snippets = Passes.objects.all()
        serializer = PassesSerializerAll(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PassesSerializerAll(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        except:
            return Response([{"status": "failed"}])

# Δεν δουλευει με απλο path το open για καποιο λογο
# οποτε εβαλα το full path του δικου μου υπολογιστη
# Δε θα σας δουλευει αν δεν αλλαξετε το path


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
