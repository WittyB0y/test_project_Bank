from rest_framework import serializers
from .models import Wallet


class UserWalletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class AllUserWalletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on',)
