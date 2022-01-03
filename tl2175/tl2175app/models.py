from django.db import models
from import_export import resources

# Create your models here.


class Provider(models.Model):
    providerAbbr = models.CharField(max_length=2, unique=True)
    providerName = models.CharField(
        max_length=50, unique=True, primary_key=True)  # primary
    iban = models.CharField(max_length=50)
    bankname = models.CharField(max_length=50)

    def __str__(self):
        return self.providerName + ' (' + self.providerAbbr + ')'


class Station(models.Model):
    stationid = models.CharField(
        max_length=4, primary_key=True, default='')  # primary
    stationProvider = models.CharField(max_length=50)
    #stationProvider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    stationName = models.CharField(max_length=50)
    # provider = Provider.objects.get(providerName=stationProvider)
    fk = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE, default='')
            
    def __str__(self):
        return self.stationName #+ ' (' + self.fk.providerAbbr+')'

class Vehicle(models.Model):
    vehicleid = models.CharField(
        max_length=12, unique=True, primary_key=True)  # primary
    tagid = models.CharField(max_length=9, unique=True)
    licenceYear = models.IntegerField()
    tagProvider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name='tagProvider', default=' ')
    tagProviderAbbr = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name='tagProviderAbbr', null=True, to_field='providerAbbr')

    def __str__(self):
        return self.vehicleid


class Passes(models.Model):
    passid = models.CharField(max_length=20, primary_key=True)  # primary
    timestamp = models.DateTimeField()
    charge = models.DecimalField(max_digits=5, decimal_places=2)
    stationRef = models.ForeignKey(
        Station, on_delete=models.CASCADE)
    vehicleRef = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.passid



