from django.urls import path, include
from rest_framework import routers
from .views import Wallets_data, detail_wallet

router = routers.DefaultRouter()
router.register(r'wallets', Wallets_data)

urlpatterns = [
    path('wallet/<slug:slug>/', detail_wallet),
    path('', include(router.urls)),
]
