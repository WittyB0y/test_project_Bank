from django.urls import path, include
from rest_framework import routers
from .views import Wallets_data

router = routers.DefaultRouter()
router.register(r'wallets',Wallets_data)
print(router)

urlpatterns = [
    path('', include(router.urls)),
]
