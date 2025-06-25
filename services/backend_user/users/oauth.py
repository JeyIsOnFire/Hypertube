from abc import abstractmethod
import requests
import os
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import UserOAuthRegisterSerializer


class OAuth:
    client_id = None
    client_secret = None
    redirect_uri = None

    api_token_url = None
    api_user_url = None
    access_token = None

    @abstractmethod
    def set_token(self, code):
        pass

    @abstractmethod
    def get_user(self, code):
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
    def __init__(self):
        self.client_id = os.getenv("OAUTH_42_CLIENT")
        self.client_secret = os.getenv("OAUTH_42_SECRET")
        self.redirect_uri = os.getenv("OAUTH_42_REDIRECTION")

        self.api_token_url = "https://api.intra.42.fr/oauth/token"
        self.api_user_url = "https://api.intra.42.fr/v2/me"

    def set_token(self, code):
        paylod = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        response = requests.post(self.api_token_url,
                                 headers={"Content-Type": "application/json"},
                                 json=paylod)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.text}")

        self.access_token = response.json()['access_token']

    def get_user(self, code):
        self.set_token(code)

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


class OAuthGoogle(OAuth):
    def __init__(self):
        self.client_id = os.getenv("OAUTH_GOOGLE_CLIENT")
        self.client_secret = os.getenv("OAUTH_GOOGLE_SECRET")
        self.redirect_uri = os.getenv("OAUTH_GOOGLE_REDIRECTION")

        self.api_token_url = "https://oauth2.googleapis.com/token"
        self.api_user_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    def set_token(self, code):
        paylod = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        response = requests.post(self.api_token_url,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 data=paylod)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.text}")

        self.access_token = response.json()['access_token']

    def get_user(self, code):
        self.set_token(code)

        response = requests.get(self.api_user_url,
                                headers={'Authorization': 'Bearer ' + self.access_token})

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.text}")

        response = response.json()
        print(response)
        user = {
            "oauth_id": f"google-{response['sub']}",
            "username": response['given_name'] + response['family_name'],
            "email": response['email'],
            "first_name": response['given_name'],
            "last_name": response['family_name'],
            "preferred_language": "en"
        }
        return self.serialization_from_oauth(user)


class OAuthGitHub(OAuth):
    def __init__(self):
        self.client_id = os.getenv("OAUTH_GOOGLE_CLIENT")
        self.client_secret = os.getenv("OAUTH_GOOGLE_SECRET")
        self.redirect_uri = os.getenv("OAUTH_GOOGLE_REDIRECTION")

        self.api_token_url = "https://oauth2.googleapis.com/token"
        self.api_user_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    def set_token(self, code):
        paylod = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        response = requests.post(self.api_token_url,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 data=paylod)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.text}")

        self.access_token = response.json()['access_token']

    def get_user(self, code):
        self.set_token(code)

        response = requests.get(self.api_user_url,
                                headers={'Authorization': 'Bearer ' + self.access_token})

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.text}")

        response = response.json()
        print(response)
        user = {
            "oauth_id": f"google-{response['sub']}",
            "username": response['given_name'] + response['family_name'],
            "email": response['email'],
            "first_name": response['given_name'],
            "last_name": response['family_name'],
            "preferred_language": "en"
        }
        return self.serialization_from_oauth(user)


oauth_42_instance = OAuth42()
oauth_google_instance = OAuthGoogle()
oauth_github_instance = OAuthGitHub()

