from rest_framework import serializers
from .models import Ticket
from flights.serializers import FlightSerializer

class TicketSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'flight', 'seat_number', 'price', 'booking_time']
        unique_together = ('flight', 'seat_number')
        
    def validate(self, data):
        flight = data.get('flight')
        
        if flight and flight.status in ['cancelled', 'departed']:
            raise serializers.ValidationError("Cannot book a ticket for a flight that is cancelled or departed.")
        
        return data