from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Wallet
from .serializers import UserWalletsSerializer, AllUserWalletsSerializer
import random
import string


def generate_random_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=8))
    return code


class Wallets_data(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()

    def retrieve(self, request, pk=None):
        if pk is not None:
            user_wallet = Wallet.objects.filter(user=request.user.id, name=pk)
            serializer = self.get_serializer(user_wallet, many=True)
            return Response(serializer.data)
        else:
            return self.list(request)

    def list(self, request):
        user_id = request.user.id
        wallets = self.queryset.filter(user=user_id)
        serializer = self.get_serializer(wallets, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        amount_wallets = Wallet.objects.filter(user=user_id).count()
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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserWalletsSerializer
        elif self.request.method == 'GET':
            return AllUserWalletsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        return Response({'error': "You can't change data!"})

    def destroy(self, request, *args, **kwargs):
        name_wallet = kwargs.get('pk', None)
        if name_wallet is not None:
            Wallet.objects.filter(user=request.user.id, name=name_wallet).delete()
            return Response({'Success': f'The wallet {name_wallet} has been removed'})
        return Response({'error': 'No access'})
