from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({
                'password': "Password fields didn't match"
            })

        password = attrs.get('password')
        if not any(char.isupper() for char in password) or \
           not any(char.islower() for char in password) or \
           not any(char.isdigit() for char in password):
            raise serializers.ValidationError({
                'password': '密碼必須包含大小寫字母和數字'
            })

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user