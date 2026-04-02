from django.contrib import admin
from .models import Seat, Order, Ticket

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'seat_number', 'seat_class', 'price')
    list_filter = ('seat_class', 'price')
    search_fields = ('seat_number',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flight', 'total_price', 'currency', 'status', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at', 'status')
    search_fields = ('user__email', 'flight__flight_number')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'get_user', 'get_flight', 'ticket_number', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('order__user__email', 'order__flight__flight_number', 'ticket_number')
    
    def get_user(self, obj):
        return obj.order.user.email
    get_user.short_description = 'User'
    
    def get_flight(self, obj):
        return obj.order.flight.flight_number
    get_flight.short_description = 'Flight'



