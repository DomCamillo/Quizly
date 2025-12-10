from django.urls import path
from .views import RegistrationView, LoginTokenView, LogoutView, RefreshTokenView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

]

