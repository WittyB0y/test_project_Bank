from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as DbUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = DbUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        token_key = response.data['token']

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=400)

        return Response({'token': token.key})


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'detail': 'Successfully logged out.'})
        except Token.DoesNotExist:
            Response({'error': 'Invalid token'}, status=400)
