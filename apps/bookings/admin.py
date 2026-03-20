from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flight', 'seat_number', 'price', 'booking_time')
    list_filter = ('booking_time',)
    search_fields = ('user__username', 'flight__flight_number', 'seat_number')



