from django.contrib import admin
from .models import Airport, Flights,Passenger
# Register your models here.

admin.site.register(Airport)
admin.site.register(Flights)
admin.site.register(Passenger)