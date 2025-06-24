from abc import ABC, abstractmethod
import requests
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import UserOAuthRegisterSerializer


class OAuth:
    paylod = {"grant_type": "authorization_code", "redirect_uri": "https://localhost:8443/users/connect-oauth/"}
    headers = {"Content-Type": "application/json"}
    api_token_url = None
    api_user_url = None
    access_token = None

    @abstractmethod
    def set_token(self):
        pass

    @abstractmethod
    def get_user(self):
        pass

    def serialization_from_oauth(self, user_data):
        if User.objects.filter(oauth_id=user_data["oauth_id"]).exists():
            user = User.objects.get(oauth_id=user_data["oauth_id"])
        else:
            serializer = UserOAuthRegisterSerializer(data=user_data)

            if serializer.is_valid():
                user = serializer.save()
            else:
                raise ValidationError(serializer.errors)
        return user


class OAuth42(OAuth):
    def __init__(self, code):
        self.paylod["code"] = code
        self.paylod["client_id"] = "u-s4t2ud-2c90b78954c87807b2c6a5381a3d1923e0737de30580e8b2a27f0ee0cdb97460"
        self.paylod["client_secret"]= "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"

        self.api_token_url = "https://api.intra.42.fr/oauth/token"
        self.api_user_url = "https://api.intra.42.fr/v2/me"

        self.set_token()

    def set_token(self):
        response = requests.post(self.api_token_url,
                                 headers=self.headers,
                                 json=self.paylod)
        self.access_token = response.json()['access_token']

    def get_user(self):
        response = requests.get(self.api_user_url,
                                headers={'Authorization': 'Bearer ' + self.access_token})

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.text}")

        response = response.json()
        print(response)
        user = {
            "oauth_id": f"42-{response['id']}",
            "username": response['login'],
            "email": response['email'],
            "first_name": response['first_name'],
            "last_name": response['last_name'],
            "preferred_language": "en"
        }
        return self.serialization_from_oauth(user)