from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import models
from .models import Seat, Order, Ticket
from .serializers import SeatSerializer, OrderSerializer, TicketSerializer


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Seat.objects.all()
        
        flight_id = self.request.query_params.get('flight')
        is_available = self.request.query_params.get('is_available')
        
        if flight_id:
            queryset = queryset.filter(flight_id=flight_id)
        
        if is_available and is_available.lower() == 'true':
            now = timezone.now()

            taken_seats_ids = Ticket.objects.filter(
                models.Q(order__status='paid') | 
                models.Q(order__status='pending', order__expires_at__gt=now)
            ).values_list('seat_id', flat=True)

            queryset = queryset.exclude(id__in=taken_seats_ids)
        
        return queryset


class OrderViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet,
                    ):

    serializer_class = OrderSerializer  
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('tickets__seat')
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object() 
        
        if order.status == 'pending' and timezone.now() > order.expires_at:
            order.status = 'cancelled'
            order.save()
            return Response({'detail': 'Order has expired and is now cancelled.'}, status=400)
        
        if order.status != 'pending':
            return Response({'detail': 'This order is already paid or cancelled.'}, status=400)
        
        order.status = 'paid'
        order.save()
        
        return Response({'detail': 'Order has been paid successfully.'}, status=200)

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Ticket.objects.filter(
            order__user=self.request.user,
            order__status='paid'
        ).select_related('order__flight', 'seat')

