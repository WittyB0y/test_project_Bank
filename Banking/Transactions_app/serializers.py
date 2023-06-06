from rest_framework import serializers
from .models import Transaction


class NewTransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(read_only=True)
    receiver = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('sender', 'receiver', 'transfer_amount',)


class GetAllTransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(read_only=True)
    receiver = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
