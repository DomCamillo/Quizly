from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class RegistrationView(APIView):
    """"Simple user registration view"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
            {"detail": "User created successfully!"},
            status=status.HTTP_201_CREATED
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    View to handle user logout by deleting JWT cookies.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
       response = Response()
       response.delete_cookie('access_token')
       response.delete_cookie('refresh_token')
       response.data = {'message' : 'Sucessfully logged out'}
       return response


class LoginTokenView(TokenObtainPairView):
    """
    Custom Login View that sets JWT tokens in HttpOnly cookies upon successful authentication.
    sercure=False for development purposes only to use localhost. In production, set secure=True
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data.get('username'))
        refresh = response.data.get('refresh')
        access = response.data.get('access')


        response.set_cookie(
            key="access_token",
            httponly=True,
            secure=False,
            value=str(access),
            samesite='Lax'
        ),
        response.set_cookie(
            key="refresh_token",
            httponly=True,
            secure=False,
            value=str(refresh),
            samesite='Lax'
        )

        response.data = {
            "detail": "Login successfully!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
        return response



class RefreshTokenView(TokenRefreshView):
    """
    Custom Token Refresh View that reads the refresh token from HttpOnly cookies
    and sets a new access token in HttpOnly cookies.
    """
def post(self, request, *args, **kwargs):
     refresh_token =request.COOKIES.get('refresh_token')

     if refresh_token is None:
         return Response({"detial": "Refresh token not found"}, status=400)



     request.data['refresh'] = refresh_token
     serializer = self.get_serializer(data={'refresh': refresh_token})

     try: serializer.is_valid(raise_exception=True)
     except:
         return Response({"detail": "Invalid refresh token "}, status=401)

     access_token = serializer.validated_data.get("access")

     response = Response({
        "detail": "Token refreshed",
        "access": access_token
     })
     response.set_cookie(
            key="access_token",
            httponly=True,
            value=access_token,
            secure=False,
            samesite='Lax'
        ),
     return response

















