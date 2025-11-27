from django.urls import path

from .views import RegistrationView, JWTTEstView, LoginTokenView, LogoutView, RefreshTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('jwt-test/', JWTTEstView.as_view(), name='jwt_test'),

]

