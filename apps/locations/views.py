from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny


from .serializers import CountrySerializer, AirportSerializer
from .models import Country, Airport


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    
class AirportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [AllowAny]