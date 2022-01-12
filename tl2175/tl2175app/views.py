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
from django.views.decorators.csrf import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from drf_multiple_model.views import ObjectMultipleModelAPIView


def transportation(request):
    if request.method == 'POST':
        #form = MemberForm(request.POST or None)
        operator1 = request.POST['operator1']
        operator2 = request.POST['operator2']
        datefrom = request.POST['datefrom']
        dateto = request.POST['dateto']

        posts = Passes.objects.raw("""
            select pass.*
            FROM
            	providers prov
            	passes pass
            	vehicles veh
            	station
            where
            	pass.timestamp BETWEEN datefrom and dateto
            	AND pass.stationRef = station.providerName
            	AND station.providerName = prov.providerName
            	AND prov.providerName = operator1
            	AND pass.vehicleRef = veh.vehicleid
            	AND veh.tagProvider = operator2""")


        return render(request, 'transportation.html', {'data':posts})
    return render(request, 'transportation.html', {})



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
                    value.stationProvider = data[1]
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
                    value.tagProvider = data[2]
                    value.tagProviderAbbr = data[3]
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
                    value.stationRef = data[2]
                    value.vehicleRef = data[3]
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
        index=0
        for data in serializer.data :
            index+=1
            Vehicle = passes[index-1].passes_fk2
            Vehicle_tagProvider = Vehicle.tagProvider
            data["PassIndex"] = index
            data["TagProvider"] = Vehicle_tagProvider
            data.pop("stationRef")
        
        return Response(serializer.data)
