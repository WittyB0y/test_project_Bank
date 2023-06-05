from django.contrib.auth.models import User as dbUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = dbUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        new_user = dbUser.objects.create_user(**validated_data)
        return new_user
