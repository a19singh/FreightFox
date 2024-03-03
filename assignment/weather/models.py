from django.db import models

class Location(models.Model):
    """
    Django model to save location of the query 
    and queried timestamp
    """
    pincode = models.IntegerField(max_length=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    cdate = models.DateTimeField(auto_now_add=True)

class Weather(models.Model):
    """
    Store weather info for a particular date.
    """
    date = models.DateField()
    pincode = models.ForeignKey(Location, on_delete=models.CASCADE)
    data = models.TextField() 
