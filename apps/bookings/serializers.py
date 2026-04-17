from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from rest_framework import serializers

from django.db import models
from .models import Seat, Order, Ticket
from flights.serializers import FlightSerializer

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'seat_class', 'price']

class OrderSerializer(serializers.ModelSerializer):
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True,
    )    
    
    class Meta:
        model = Order
        fields = ['id', 'flight', 'seat_ids', 'total_price', 'currency', 'status', 'created_at', 'expires_at']
        read_only_fields = ['id', 'total_price', 'currency', 'status', 'created_at', 'expires_at']

    def validate(self, data):
        flight = data.get('flight')
        seat_ids = data.get('seat_ids', [])
        
        now = timezone.now()
        
        seats = Seat.objects.filter(id__in=seat_ids, flight=flight)
        
        if len(seats) != len(seat_ids):
            raise serializers.ValidationError("One or more selected seats are invalid for this flight.")
        
        if flight and flight.status in ['cancelled', 'departed']:
            raise serializers.ValidationError("Cannot book a ticket for a flight that is cancelled or departed.")
        
        taken_seats = Ticket.objects.filter(seat__in=seats).filter(
            models.Q(order__expires_at__gt=now) | models.Q(order__status='paid') | models.Q(order__status='pending')
        ).exists()
        
        if taken_seats:
            raise serializers.ValidationError("One or more selected seats are already booked.")
        
        data['seats_objects'] = seats
        return data

    @transaction.atomic
    def create(self, validated_data):
        seats = validated_data.pop('seats_objects', [])
        flight = validated_data['flight']
        
        total_price = sum(seat.price for seat in seats)
        currency = flight.currency
        
        order = Order.objects.create(
            user=self.context['request'].user,
            flight=flight,
            total_price=total_price,
            currency=currency,
            status='pending',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        Ticket.objects.bulk_create([
            Ticket(order=order, seat=seat, ticket_number=f"TKT-{order.id}-{seat.id}") for seat in seats
        ])
        
        return order


class TicketSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'order', 'seat', 'ticket_number', 'issued_at']
        read_only_fields = ['id', 'order', 'seat', 'ticket_number', 'issued_at']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['flight'] = FlightSerializer(instance.order.flight).data
        return representation