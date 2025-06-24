from datetime import datetime, timedelta

import jwt
import requests
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from app import settings
from users.models import User
from users.serializers import UserRegisterSerializer, UserOAuthRegisterSerializer


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        return user, None

def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=7),  # Token valid for 7 days (need to be update)
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def generate_response_with_token(user, delay):
    response = Response({'success': True})
    response.set_cookie(
        key='access_token',
        value=generate_token(user),
        httponly=True,
        max_age=delay
    )
    return response


def generate_redirection_with_token(user, delay):
    response = redirect("/")
    response.set_cookie(
        key='access_token',
        value=generate_token(user),
        httponly=True,
        max_age=delay
    )
    return response


def oauth_42_get_user(code):

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
    "grant_type": "authorization_code",
    "client_id": "u-s4t2ud-2c90b78954c87807b2c6a5381a3d1923e0737de30580e8b2a27f0ee0cdb97460",
    "client_secret": "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",
    "code": code,
    "redirect_uri": "https://localhost:8443/users/connect-oauth/"
    }

    response = requests.post("https://api.intra.42.fr/oauth/token", headers=headers, json=payload)

    access_token = response.json()['access_token']

    response = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': 'Bearer ' + access_token})
    print(response.status_code)
    print(response.text)

    response = response.json()

    user = {
        "username": response['login'],
        "email": response['email'],
        "first_name": response['first_name'],
        "last_name": response['last_name'],
        "preferred_language": "en"
    }

    serializer = UserOAuthRegisterSerializer(data=user)

    if serializer.is_valid():
        user = serializer.save()
        return generate_redirection_with_token(user, 150000)
    else:
        raise ValidationError(serializer.errors)