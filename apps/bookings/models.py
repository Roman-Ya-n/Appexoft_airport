from django.db import models
from django.core.validators import MinValueValidator

from config import settings
from flights.models import Flight

class Seat(models.Model):
    CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    seat_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ('flight', 'seat_number')
    
    def __str__(self):
        return f"{self.seat_number} ({self.seat_class}) - {self.price} {self.flight.currency}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('cancelled', 'cancelled'),
    ]   
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
        
    def __str__(self):  
        return f"Order {self.id} | {self.user.username} | {self.flight.flight_number}"

class Ticket(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    ticket_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ticket {self.ticket_number} | Order {self.order.id}"