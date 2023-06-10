from django.urls import path, include
from rest_framework import routers
from .views import WalletsData

router = routers.DefaultRouter()
router.register(r'wallets', WalletsData)

urlpatterns = [
    path('', include(router.urls)),
]
