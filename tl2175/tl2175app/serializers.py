from rest_framework import serializers
from .models import *


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('providerAbbr', 'providerName', 'iban', 'bankname')

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('stationid', 'stationProvider',
                  'stationName', 'station_fk')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('vehicleid', 'tagid', 'licenceYear',
                  'tagProvider', 'tagProviderAbbr', 'vehicle_fk1')

class PassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passes
        fields = ('passid', 'timestamp', 'charge', 'stationRef',
                  'vehicleRef', 'pass_type')    
