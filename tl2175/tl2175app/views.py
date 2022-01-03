from django.shortcuts import render
from .models import Vehicle, Passes, Station, Provider

# Create your views here.

from .resources import StationResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse

def upload_from_xslsx(request):
    if request.method == 'POST':
        station_resource = StationResource()
        dataset = Dataset()
        new_station = request.FILES['myfile'] 

        if not new_station.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'upload.html')
        
        imported_data = dataset.load(new_station.read(), format='xlsx')
        for data in imported_data:
            value = Station(
                data[0],
                data[1],
                data[2],
                Provider.objects.get(providerName=data[1])
            )
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
