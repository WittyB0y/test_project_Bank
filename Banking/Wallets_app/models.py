from enum import Enum
from django.db import models
from rest_framework.authtoken.admin import User


class WalletType(Enum):
    VISA = 'Visa'
    MASTERCARD = 'Mastercard'


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    RUB = 'RUB'


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=8, unique=True)
    type = models.CharField(max_length=10, choices=[(t.name, t.value) for t in WalletType])
    currency = models.CharField(max_length=3, choices=[(c.name, c.value) for c in Currency])
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name