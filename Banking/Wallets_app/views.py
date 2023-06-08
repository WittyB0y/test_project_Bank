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

    def get_queryset(self, param, data=None) -> Wallet:
        match param:
            case 'POST':
                return Wallet.objects.filter(user=data).count()
            case 'GET':
                return Wallet.objects.filter(user=data.get('user'), name=data.get('name'))
            case 'DELETE':
                print(Wallet.objects.filter(user=data.get('user'), name=data.get('name')))
                return Wallet.objects.filter(user=data.get('user'), name=data.get('name')).delete()
            case _:
                return super().get_queryset()

    def retrieve(self, request, pk=None):
        if pk is not None:
            data = {'user': request.user.id, 'name': pk}
            user_wallet = self.get_queryset(self.request.method, data)
            serializer = self.get_serializer(user_wallet, many=True)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request) -> Response:
        user_id = request.user.id
        wallets = self.get_queryset('list').filter(user=user_id)
        serializer = self.get_serializer(wallets, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs) -> Response:
        try:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            amount_wallets = self.get_queryset(self.request.method, user_id)
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
            data = {'user': request.user.id, 'name': name_wallet}
            self.get_queryset(request.method, data)
            return Response({'Success': f'The wallet {name_wallet} has been removed'})
        return Response({'error': 'No access'})