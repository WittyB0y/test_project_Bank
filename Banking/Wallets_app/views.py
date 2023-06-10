from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Wallet
from .serializers import UserWalletsSerializer, AllUserWalletsSerializer
import random
import string


def generate_random_code() -> str:
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=8))
    return code


class WalletsData(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_classes = {
        'POST': UserWalletsSerializer,
        'GET': AllUserWalletsSerializer,
    }

    def get_queryset(self) -> Wallet:
        method = self.request.method
        user = self.request.user.id
        name_wallet = self.request.resolver_match.kwargs.get('pk')
        match method:
            case 'POST':
                return Wallet.objects.filter(user=user)
            case 'GET':
                if not name_wallet:
                    return Wallet.objects.filter(user=user)
                return Wallet.objects.filter(user=user, name=name_wallet)
            case 'DELETE':
                return Wallet.objects.filter(user=user, name=name_wallet)
            case _:
                return super().get_queryset()

    def retrieve(self, request, pk=None):
        if pk is not None:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        else:
            return self.list(request)

    def create(self, request, *args, **kwargs) -> Response:
        try:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            amount_wallets = self.get_queryset().count()
            if amount_wallets <= 5:
                wallet = Wallet(
                    name=generate_random_code(),
                    user=user,
                    type=request.data['type'],
                )

                if request.data['currency'] == 'USD' or request.data['currency'] == 'EUR':
                    wallet.balance = Decimal('3.00')
                elif request.data['currency'] == 'RUB':
                    wallet.balance = Decimal('100.00')

                wallet.save()
                serializer = UserWalletsSerializer(wallet)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': '5 wallets are the max value'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'})

    def get_serializer_class(self) -> serializer_classes:
        return self.serializer_classes.get(self.request.method) or super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs) -> Response:
        name_wallet = kwargs.get('pk', None)
        if name_wallet is not None:
            self.get_queryset().delete()
            return Response({'Success': f'The wallet {name_wallet} has been removed'})
        return Response({'error': 'No access'})