from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(mixins.ListModelMixin, 
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)      
        


