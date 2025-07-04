# services/backend_user/users/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_picture',
            'preferred_language'
        ]
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['oauth_id', 'id', 'username', 'email', 'first_name', 'last_name',
                  'profile_picture', 'preferred_language']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'preferred_language']

    def create(self, validated_data):
        print("Creating user with data:", validated_data)
        return User.objects.create_user(**validated_data)

class UserOAuthRegisterSerializer(serializers.ModelSerializer):
    oauth_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['oauth_id', 'username', 'email', 'first_name', 'last_name', 'preferred_language']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_unusable_password()
        user.save()
        print("Creating OAuth user with data:", validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_picture',
            'preferred_language'
            ]

        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile_picture': {'required': False},
            'preferred_language': {'required': False},
        }
