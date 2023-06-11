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
        'create': UserWalletsSerializer,
        'list': AllUserWalletsSerializer,
        'retrieve': AllUserWalletsSerializer,
    }
    lookup_field = 'name'

    def get_queryset(self) -> Wallet:
        user = self.request.user.id
        name_wallet = self.kwargs.get(self.lookup_field)
        match self.action:
            case 'list':
                return Wallet.objects.filter(user=user)
            case 'retrieve':
                return Wallet.objects.filter(**{self.lookup_field: name_wallet})
            case 'create':
                return Wallet.objects.filter(user=user)
            case 'destroy':
                return Wallet.objects.filter(user=user, **{self.lookup_field: name_wallet})
            case _:
                return super().get_queryset()

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
                wallet.currency = request.data['currency']
                wallet.save()
                serializer = UserWalletsSerializer(wallet)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': '5 wallets are the max value'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'})

    def get_serializer_class(self) -> serializer_classes:
        return self.serializer_classes.get(self.action) or super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs) -> Response:
        name_wallet = kwargs.get('name', None)
        if name_wallet is not None:
            self.get_queryset().delete()
            return Response({'Success': f'The wallet {name_wallet} has been removed'})
        return Response({'error': 'No access'})
