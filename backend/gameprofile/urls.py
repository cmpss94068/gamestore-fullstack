from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gameprofile.views import profilePostView, platformView, categoryView

app_name = 'gameprofile'

router = DefaultRouter()
router.register('profilePost', viewset=profilePostView, basename='profilePost')
router.register('platform', viewset=platformView, basename='platform')
router.register('category', viewset=categoryView, basename='category')

urlpatterns = [
    path('', include((router.urls, app_name), namespace='gameprofile')),
]
