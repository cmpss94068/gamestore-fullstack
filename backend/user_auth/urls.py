from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'user_auth'

router = DefaultRouter()
router.register('register', viewset=RegisterationView, basename='register')

urlpatterns = [
    path('', include((router.urls, app_name), namespace='user_auth')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
