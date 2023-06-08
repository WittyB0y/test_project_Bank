from django.db import models
from Wallets_app.models import Wallet


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='received_transactions')
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)