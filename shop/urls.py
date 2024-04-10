from django.urls import path,include
from rest_framework.routers import DefaultRouter
from shop.api import ShopUserViewSet,ShopViewSet,ConsumerViewSet,PaymentViewSet

router = DefaultRouter()
router.register('api/shopuser', ShopUserViewSet, basename='shopuser')
router.register('api/shop',ShopViewSet,basename='shop')
router.register('api/consumer',ConsumerViewSet,basename='consumer')
router.register('api/payment',PaymentViewSet,basename='payment')

urlpatterns=router.urls


