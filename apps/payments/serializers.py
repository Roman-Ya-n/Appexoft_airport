from rest_framework import serializers
from payments.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'stripe_session_id', 'status', 'amount', 'currency', 'created_at']
        
    
