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

    @abstractmethod
    def generate_payload(self, code):
        pass

    def generate_access_token(self, headers, payload, payload_type="json"):
        if payload_type == 'data':
            response = requests.post(self.api_token_url,
                                 headers=headers,
                                 data=payload)
        else:
            response = requests.post(self.api_token_url,
                                     headers=headers,
                                     json=payload)

        if response.status_code != 200:
            print("OAuth: Access token failed")
            return None

        access_token = response.json()['access_token']
        return access_token

    def generate_user_data(self, access_token):
        response = requests.get(self.api_user_url,
                                headers={'Authorization': 'Bearer ' + access_token})

        if response.status_code != 200:
            print("OAuth: User data failed")
            return None

        response = response.json()
        return response

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

    def generate_payload(self, code):
        return {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }

    def get_user(self, code):
        payload = self.generate_payload(code)
        access_token = self.generate_access_token({"Content-Type": "application/json"}, payload)
        if access_token is None:
            return None
        user_data = self.generate_user_data(access_token)
        if user_data is None:
            return None

        user = {
            "oauth_id": f"42-{user_data['id']}",
            "username": user_data['login'],
            "email": user_data['email'],
            "first_name": user_data['first_name'],
            "last_name": user_data['last_name'],
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

    def generate_payload(self, code):
        return {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }

    def get_user(self, code):
        payload = self.generate_payload(code)
        access_token = self.generate_access_token({"Content-Type": "application/x-www-form-urlencoded"}, payload, "data")
        if access_token is None:
            return None
        user_data = self.generate_user_data(access_token)
        if user_data is None:
            return None

        user = {
            "oauth_id": f"google-{user_data['sub']}",
            "username": user_data['given_name'] + user_data['family_name'],
            "email": user_data['email'],
            "first_name": user_data['given_name'],
            "last_name": user_data['family_name'],
            "preferred_language": "en"
        }
        return self.serialization_from_oauth(user)


class OAuthGitHub(OAuth):
    def __init__(self):
        self.client_id = os.getenv("OAUTH_GITHUB_CLIENT")
        self.client_secret = os.getenv("OAUTH_GITHUB_SECRET")
        self.redirect_uri = os.getenv("OAUTH_GITHUB_REDIRECTION")

        self.api_token_url = "https://github.com/login/oauth/access_token"
        self.api_user_url = "https://api.github.com/user"

    def generate_payload(self, code):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }

    def get_user(self, code):
        payload = self.generate_payload(code)
        access_token = self.generate_access_token({"Accept": "application/json"}, payload)
        if access_token is None:
            return None
        user_data = self.generate_user_data(access_token)
        if user_data is None:
            return None

        user = {
            "oauth_id": f"github-{user_data['id']}",
            "username": user_data['login'],
            "email": user_data['email'] if user_data.get('email') else "email@private.com",
            "first_name": user_data['name'] if user_data.get('name') else "Unknown",
            "last_name": user_data['name'] if user_data.get('name') else "Unknown",
            "preferred_language": "en"
        }
        return self.serialization_from_oauth(user)


oauth_42_instance = OAuth42()
oauth_google_instance = OAuthGoogle()
oauth_github_instance = OAuthGitHub()

