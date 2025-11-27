from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer #CostumeTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            data = {
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    pass

class LoginTokenView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get('refresh')
        access = response.data.get('access')

        response.set_cookie(
            key="access_token",
            httponly=True,
            secure=True,
            value=str(access),
            samesite='Lax'
        ),
        response.set_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            value=str(refresh),
            samesite='Lax'
        )

        response.data={"login": "successfully"}
        return response



class RefreshTokenView(TokenRefreshView):
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

     response = Response({"message": "access token refreshed successfully"})
     response.set_cookie(
            key="access_token",
            httponly=True,
            value=access_token,
            secure=True,
            samesite='Lax'
        ),
     return response


class JWTTEstView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "JWT is working!"})



# class CookieALoginTokenView(TokenObtainPairView):
#     """
#     An endpoint for obtaining JWT tokens and storing them in HttpOnly cookies.
#     works with email and password isntead of username
#     """
#     serializer_class = CostumeTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         response = Response({"message": "Login Successfull"})

#         refresh = serializer.validated_data['refresh']
#         access = serializer.validated_data['access']

#         response.set_cookie( #Speichere diesen Token in einem HttpOnly-Cookie namens access_token
#             key="acces_token",
#             httponly=True,
#             value=str(access),
#             secure=True,
#             samesite='Lax'
#         ),
#         response.set_cookie(
#             key="refresh_token",
#             httponly=True,
#             value=str(refresh),
#             secure=True,
#             samesite='Lax'
#         )
#         #response.set_cookie() ist eine Django-Funktion, mit der du dem Browser Cookies mitschickst.
#         #Diese Cookies werden danach automatisch vom Browser gespeichert und bei jedem zukünftigen Request automatisch wieder mitgeschickt.

#         response.data={"login": "successfully"}
#         return response











