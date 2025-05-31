from datetime import datetime, timedelta

import jwt
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from app import settings
from users.models import User


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

        return (user, None)

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