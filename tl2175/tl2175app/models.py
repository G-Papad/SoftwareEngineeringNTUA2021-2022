from django.db import models
from import_export import resources

# Create your models here.


class Provider(models.Model):
    providerAbbr = models.CharField(max_length=2, unique=True)
    providerName = models.CharField(
        max_length=50, unique=True)  # primary
    iban = models.CharField(max_length=50)
    bankname = models.CharField(max_length=50)

    def __str__(self):
        return self.providerName + ' (' + self.providerAbbr + ')'


class Station(models.Model):
    stationid = models.CharField(
        max_length=4, default='')  # primary
    # stationProvider = models.CharField(max_length=50)
    stationName = models.CharField(max_length=50)
    station_fk = models.ForeignKey(Provider, null=True,
                                   on_delete=models.CASCADE, default='', db_constraint=False)

    def __get_stationProvider(self):
        return self.station_fk.providerName

    stationProvider = property(__get_stationProvider)

    def __str__(self):
        return self.stationName  # + ' (' + self.fk.providerAbbr+')'

class Vehicle(models.Model):
    vehicleid = models.CharField(
        max_length=12, unique=True)  # primary
    tagid = models.CharField(max_length=9, unique=True)
    licenceYear = models.IntegerField()
    # tagProvider = models.CharField(max_length=50)
    # tagProviderAbbr = models.CharField(max_length=2)

    vehicle_fk1 = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name='tagProvider', default='', db_constraint=False)

    def __get_tagProvider(self):
        return self.vehicle_fk1.providerName

    def __get_tagProviderAbbr(self):
        return self.vehicle_fk1.providerAbbr

    tagProvider = property(__get_tagProvider)
    tagProviderAbbr = property(__get_tagProviderAbbr)

    def __str__(self):
        return self.vehicleid

class Passes(models.Model):
    passid = models.CharField(max_length=20, null=True)  # primary
    timestamp = models.DateTimeField()
    charge = models.DecimalField(max_digits=5, decimal_places=2)
    # stationRef = models.CharField(max_length=50)
    # vehicleRef = models.CharField(max_length=12)
    passes_fk1 = models.ForeignKey(
        Station, on_delete=models.CASCADE, default='', db_constraint=False)
    passes_fk2 = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, default='', db_constraint=False)
    
    def __get_pass_type(self):
        if(self.passes_fk1.stationProvider == self.passes_fk2.tagProvider):
            return "home"
        return "visitor"

    def __get_stationRef(self):
        return self.passes_fk1.stationName
    
    def __get_vehicleRef(self):
        return self.passes_fk2.vehicleid

    pass_type = property(__get_pass_type)
    stationRef = property(__get_stationRef)
    vehicleRef = property(__get_vehicleRef)

    def __str__(self):
        return self.passid
