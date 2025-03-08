from django.urls import path
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView


apidoc_urlpatterns = [
  path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('test/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
  # Auth API
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/partner/login/', PartnerTokenObtainPairView.as_view(), name='partner_login'),
    path('auth/partner/register/', PartnerRegistrationView.as_view(), name='partner_register'),
    
  # Venue Data API
    path('venue/data/', VenueDataView.as_view(), name='venue_data'),
    path('venue/create/', CreatePartnerProfileView.as_view(), name='create_venue'),
    
  # Data Collect API
    path('data/collect/', DataCollectView.as_view(), name='data_collect'),
    
  # Release App API
    path('release/app/', ReleaseAppViewSet.as_view(), name='release_app'),

] + apidoc_urlpatterns

