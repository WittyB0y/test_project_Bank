from django.urls import path
from .views import NewTransaction, DetailTransaction, TransactionsInWallet

urlpatterns = [
    path('', NewTransaction.as_view()),
    path('<int:id>/', DetailTransaction.as_view()),
    path('<str:wallet>/', TransactionsInWallet.as_view()),
]