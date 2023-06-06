from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from Wallets_app.models import Wallet
from .models import Transaction
from Transactions_app.serializers import NewTransactionSerializer, GetAllTransactionSerializer


class NewTransaction(generics.ListCreateAPIView):
    serializer_class = NewTransactionSerializer
    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewTransactionSerializer
        elif self.request.method == 'GET':
            return GetAllTransactionSerializer

    def get(self, request, *args, **kwargs) -> Response:
        all_user_transactions = Transaction.objects.filter(
            Q(sender__user=request.user) | Q(receiver__user=request.user))
        serializer = self.get_serializer(data=all_user_transactions, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs) -> Response:
        sender_name = request.data.get('sender')
        receiver_name = request.data.get('receiver')

        try:
            sender_wallet = Wallet.objects.get(name=sender_name)
            receiver_wallet = Wallet.objects.get(name=receiver_name)

            check_user_wallet = Wallet.objects.filter(user=request.user, name=request.data['receiver']).exists()
            if check_user_wallet:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.validated_data['receiver_id'] = receiver_wallet.id
                serializer.validated_data['sender_id'] = sender_wallet.id
                serializer.validated_data['commission'] = 0

                self.perform_create(serializer)
                return Response({'success': 'Transaction created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid sender or receiver wallet name'}, status=status.HTTP_400_BAD_REQUEST)
        except Wallet.DoesNotExist:
            return Response({'error': 'Invalid sender or receiver wallet name'}, status=status.HTTP_400_BAD_REQUEST)


class DetailTransaction(generics.RetrieveAPIView):
    serializer_class = GetAllTransactionSerializer
    queryset = Transaction.objects.all()

    def get(self, request, id, *args, **kwargs) -> Response:
        detail_transaction = Transaction.objects.filter(id=id).filter(
            Q(sender__user=request.user) | Q(receiver__user=request.user))
        print(detail_transaction)
        if detail_transaction:
            serializer = self.get_serializer(detail_transaction, many=True)
            return Response(serializer.data)
        return Response({'error': 'no access'})


class TransactionsInWallet(generics.ListAPIView):
    serializer_class = GetAllTransactionSerializer
    queryset = Transaction.objects.all()

    def get(self, request, wallet, *args, **kwargs) -> Response:
        detail_transaction = Transaction.objects.filter(
            Q(sender__name=wallet) | Q(receiver__name=wallet)
        )
        if detail_transaction:
            serializer = self.get_serializer(detail_transaction, many=True)
            return Response(serializer.data)
        return Response({'error': 'no access'})
