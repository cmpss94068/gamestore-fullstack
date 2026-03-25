from rest_framework import serializers
from gameprofile.models import profile, platform, category

class platformSerializer(serializers.ModelSerializer):
    class Meta:
        model = platform
        fields = '__all__'

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'

class profilePostSerializer(serializers.ModelSerializer):
    platform = platformSerializer(many=True)
    category = categorySerializer(many=True)

    class Meta:
        model = profile
        fields = '__all__'