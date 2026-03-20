from django.contrib import admin
from .models import Country, Airport

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'country')
    search_fields = ('name', 'code', 'city')
    list_filter = ('code',)
