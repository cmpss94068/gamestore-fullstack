from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, status
from .serializers import RegisterationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.
class RegisterationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()