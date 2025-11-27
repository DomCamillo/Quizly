from django.urls import path

from .views import RegistrationView, JWTTEstView, CookieALoginTokenView,CookieTokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('token/', CookieALoginTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('jwt-test/', JWTTEstView.as_view(), name='jwt_test'),

]

