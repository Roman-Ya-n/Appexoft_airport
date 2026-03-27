from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking, Ticket
from .serializers import BookingSerializer, TicketSerializer

class BookingViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet,
                    ):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')
        
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        booking = self.get_object() 
        
        if booking.status != 'pending':
            return Response({"error": "Це бронювання вже оплачено або скасовано."}, status=400)
            
        booking.status = 'paid'
        booking.save()
        
        ticket = Ticket.objects.create(
            booking=booking,
            ticket_number=f"TKT-{booking.id}-{booking.flight.id}" 
        )
        
        return Response({
            "message": "Оплата успішна! Квиток згенеровано.", 
            "ticket_number": ticket.ticket_number
        })

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Ticket.objects.filter(booking__user=self.request.user)

