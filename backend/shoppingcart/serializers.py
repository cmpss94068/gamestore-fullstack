from rest_framework import serializers
from .models import order, orderItem
from gameprofile.serializers import profilePostSerializer

class orderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = orderItem
        fields = '__all__'

class orderSerializer(serializers.ModelSerializer):
    games = profilePostSerializer(many=True, read_only=True)

    class Meta:
        model = order
        fields = '__all__'