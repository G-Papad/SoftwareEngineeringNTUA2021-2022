from rest_framework import serializers
from .models import *


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('id', 'providerAbbr', 'providerName', 'iban', 'bankname')

    def create(self, validated_data):
        return Provider.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.providerAbbr = validated_data.get(
            'providerAbbr', instance.providerAbbr)
        instance.providerName = validated_data.get(
            'providerName', instance.providerName)
        instance.iban = validated_data.get('iban', instance.iban)
        instance.bankname = validated_data.get('bankname', instance.bankname)
        instance.save()
        return instance


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ('id', 'stationid', 'stationProvider',
                  'stationName', 'station_fk')

    def create(self, validated_data):
        return Station.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.stationid = validated_data.get(
            'stationid', instance.stationid)
        instance.stationProvider = validated_data.get(
            'stationProvider', instance.stationProvider)
        instance.stationName = validated_data.get(
            'stationName', instance.stationName)
        instance.station_fk = validated_data.get(
            'station_fk', instance.station_fk)
        instance.save()
        return instance


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'vehicleid', 'tagid', 'licenceYear',
                  'tagProvider', 'tagProviderAbbr', 'vehicle_fk1')

    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.vehicleid = validated_data.get(
            'vehicleid', instance.vehicleid)
        instance.tagid = validated_data.get('tagid', instance.tagid)
        instance.licenceYear = validated_data.get(
            'licenceYear', instance.licenceYear)
        instance.tagProvider = validated_data.get(
            'tagProvider', instance.tagProvider)
        instance.tagProviderAbbr = validated_data.get(
            'tagProviderAbbr', instance.tagProviderAbbr)
        instance.vehicle_fk1 = validated_data.get(
            'vehicle_fk1', vehicle_fk1.charge)
        instance.save()
        return instance


class PassesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passes
        fields = ('id', 'passid', 'timestamp', 'charge', 'stationRef',
                  'vehicleRef', 'passes_fk1', 'passes_fk2')
