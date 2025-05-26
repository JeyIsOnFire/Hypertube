from datetime import datetime, timedelta

import jwt
from rest_framework.response import Response

from app import settings


def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=7),  # Token valid for 7 days
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def generate_response_with_token(user, delay):
    response = Response({'success': True})
    response.set_cookie(
        key='token',
        value=generate_token(user),
        httponly=True,
        max_age=delay

    )
    return response