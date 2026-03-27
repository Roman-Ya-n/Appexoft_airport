from django.db import models
from django.core.validators import MinValueValidator

from config import settings
from flights.models import Flight

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('cancelled', 'cancelled'),
    ]   
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('flight', 'seat_number', 'status')
        

    def __str__(self):  
        return f"Booking {self.id} | {self.user.username} | {self.flight.flight_number}"

class Ticket(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='ticket', default=None, null=True, blank=True)
    ticket_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ticket {self.ticket_number} | Booking {self.booking.id}"