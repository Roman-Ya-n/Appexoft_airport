from django.db import models
from locations.models import Airport

class Airline(models.Model):
    name = models.CharField(max_length=100)
    
    airports = models.ManyToManyField(Airport, related_name='airlines')

    def __str__(self):
        return self.name
    
class Airplane(models.Model):
    model = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')
    
    def __str__(self):
        return f"{self.model} ({self.airline.name})"
