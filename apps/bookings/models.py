from django.db import models
from django.core.validators import MinValueValidator

from config import settings
from flights.models import Flight

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} | {self.user.username} | {self.flight.flight_number}"