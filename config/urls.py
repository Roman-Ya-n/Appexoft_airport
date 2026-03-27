"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from users.views import UserViewSet
from locations.views import CountryViewSet, AirportViewSet
from flights.views import FlightViewSet
from fleet.views import AirlineViewSet, AirplaneViewSet
from bookings.views import BookingViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'airports', AirportViewSet, basename='airport')
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'airlines', AirlineViewSet, basename='airline')
router.register(r'airplanes', AirplaneViewSet, basename='airplane')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [    
    path('api/', include(router.urls)),
    
    path('admin/', admin.site.urls),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
