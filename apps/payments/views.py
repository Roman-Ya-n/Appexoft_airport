from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Transaction
from .serializers import TransactionSerializer

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)



@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']['id']
        
        try:
            transaction = Transaction.objects.get(stripe_session_id=session)
            transaction.status = 'completed'
            transaction.save()
            
            order = transaction.order
            order.status = 'paid'
            order.save()
            
            
        except Transaction.DoesNotExist:
            return HttpResponse(status=404)

    return HttpResponse(status=200)
