from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that retrieves the token from cookies.
    is used in settings.py to enable cookie-based JWT authentication.
    """
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')

        if access_token is None:
            return super().authenticate(request)
        validated_token = self.get_validated_token(access_token)

        return self.get_user(validated_token), validated_token