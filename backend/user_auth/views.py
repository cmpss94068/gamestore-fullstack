from django.contrib.auth.models import User
from rest_framework import viewsets, serializers
from .serializers import RegisterationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.
class RegisterationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterationSerializer
    permission_classes = (AllowAny,)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"})

        password = attrs['password']
        if not any(char.isupper() for char in password) or \
           not any(char.islower() for char in password) or \
           not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                {"password": "不符格密碼規格，請包含大小寫英文與數字"})
        return attrs

    def create(self, request, *args, **kwargs):
        validated_data = self.validate(request.data)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return Response({'message': 'User created successfully'}, status=201)