from django.db import models

# Create your models here.


class Provider(models.Model):
    providerAbbr = models.CharField(max_length=2)
    providerName = models.CharField(max_length=13)  # primary
    iban = models.CharField(max_length=50)
    bankname = models.CharField(max_length=50)

    def __str__(self):
        return self.providerName + ' (' + self.providerAbbr + ')'


class Station(models.Model):
    stationid = models.CharField(max_length=4)  # primary
    stationProvider = models.ForeignKey(
        Provider, on_delete=models.CASCADE)
    stationName = models.CharField(max_length=50)

    def __str__(self):
        return self.stationName + ' (' + self.stationProvider.providerAbbr + ')'


class Vehicle(models.Model):
    vehicleid = models.CharField(max_length=12)  # primary
    tagid = models.CharField(max_length=9)
    licenceYear = models.IntegerField()
    tagProvider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    #providerAbbr = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return self.vehicleid


class Passes(models.Model):
    passid = models.CharField(max_length=20)  # primary
    timestamp = models.DateTimeField()
    charge = models.DecimalField(max_digits=5, decimal_places=2)
    stationRef = models.ForeignKey(Station, on_delete=models.CASCADE)
    vehicleRef = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.passid
