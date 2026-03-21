from time import timezone

from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    flight_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'status', 'airline', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'flight_duration']
        
    def get_flight_duration(self, obj):
        duration = obj.arrival_time - obj.departure_time
        return duration.total_seconds() / 3600
        
    def validate(self, data):
        if data['arrival_time'] and data['departure_time'] and data['arrival_time'] <= data['departure_time']:
            raise serializers.ValidationError("Arrival time must be after departure time.")
        
        if data['departure_airport'] == data['arrival_airport']:
            raise serializers.ValidationError("Departure and arrival airports cannot be the same.")
    
        if data['status'] == 'departed' and data['departure_time'] > timezone.now():
            raise serializers.ValidationError("Departure time cannot be in the future for a departed flight.")
        
        if data['departure_time'] and data['departure_time'] < timezone.now():
            raise serializers.ValidationError("Departure time cannot be in the past.")
        
        return data