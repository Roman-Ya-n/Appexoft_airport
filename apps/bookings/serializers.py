from rest_framework import serializers
from .models import Booking, Ticket
from flights.serializers import FlightSerializer

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'flight', 'seat_number', 'status', 'booking_time']
        read_only_fields = ['id', 'user', 'status', 'booking_time']
        
    def validate(self, data):
        flight = data.get('flight')
        
        if flight and flight.status in ['cancelled', 'departed']:
            raise serializers.ValidationError("Cannot book a ticket for a flight that is cancelled or departed.")
        
        return data

class TicketSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'booking', 'ticket_number', 'price', 'issued_at']
        read_only_fields = ['id', 'booking', 'issued_at']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['flight'] = FlightSerializer(instance.flight).data
        return representation