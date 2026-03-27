from django.contrib import admin
from .models import Booking, Ticket

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flight', 'seat_number', 'status', 'booking_time')
    list_filter = ('booking_time', 'status')
    search_fields = ('user__username', 'flight__flight_number', 'seat_number')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'ticket_number', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('booking__user__username', 'booking__flight__flight_number', 'ticket_number')
    
    def get_user(self, obj):
        return obj.booking.user.username
    get_user.short_description = 'User'
    
    def get_flight(self, obj):
        object.booking.flight.flight_number
    get_flight.short_description = 'Flight'



