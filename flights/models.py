from django.db import models
from django.views.decorators.http import last_modified

# Create your models here.
class Airport(models.Model):
    city=models.CharField(max_length=64)
    code=models.CharField(max_length=3)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flights(models.Model):
    origin=models.ForeignKey(Airport , on_delete=models.CASCADE, related_name="departures")
    destination=models.ForeignKey(Airport, on_delete=models.CASCADE ,related_name="arrivals")
    duration=models.IntegerField()

    def __str__(self):
        return f"{self.id}:from {self.origin} to {self.destination}"
    
    def is_valid_flight(self):
        return self.origin != self.destination and self.duration > 0

class Passenger(models.Model):
    first_name=models.CharField(max_length=64)
    last_name=models.CharField(max_length=64)
    flights=models.ManyToManyField(Flights ,blank=True , related_name="passenger")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    