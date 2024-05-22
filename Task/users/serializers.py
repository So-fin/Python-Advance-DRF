from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    profilepic = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        exclude = []
    
    def create(self, validated_data):
        raw = validated_data.pop('password')
        validated_data['password'] = make_password(raw)
        groups = validated_data.pop('groups', None)
        sets = validated_data.pop('user_permissions', None)
        user = User.objects.create(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    cellnumber = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        cellnumber = data.get('cellnumber')
        password = data.get('password')
        user = authenticate(cellnumber=cellnumber, password=password)
        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError("Invalid credentials")
        return data