from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import orderView

app_name = 'shoppingcart'

router = DefaultRouter()
router.register('order', viewset=orderView, basename='order')

urlpatterns = [
    path('', include((router.urls, app_name), namespace='shoppingcart')),
    path('order/<pk>/', orderView.as_view({'delete': 'destroy'}), name='order-delete'),
    path('order_count/', orderView.as_view({'get': 'cart_count'}), name='order_count')
]
