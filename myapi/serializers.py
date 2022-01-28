from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CustomUser

# SERIALIZERS FOR FUNCTION BASED VIEW

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'dob',
            'phone_no',
            'address',
            'is_staff'
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        account = CustomUser.objects.create(**validated_data)
        password = validated_data["password"]
        account.set_password(password)
        account.save()
        return account