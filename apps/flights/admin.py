from django.contrib import admin
from .models import Flight

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'status')
    list_filter = ('airline', 'status')
    search_fields = ('flight_number',)
    ordering = ('departure_time',)
