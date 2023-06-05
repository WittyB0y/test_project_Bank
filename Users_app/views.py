from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as dbUser
from rest_framework.response import Response

from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = dbUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data['token']

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=400)

        return Response({'token': token.key})