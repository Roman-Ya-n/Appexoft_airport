from django.contrib import admin
from .models import Airline, Airplane

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('model', 'capacity', 'airline')
    search_fields = ('model', 'airline__name')
    list_filter = ('airline',)
