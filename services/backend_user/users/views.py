# services/backend_user/users/views.py
from django.contrib.auth import authenticate
from django.views.decorators.http import require_GET
from rest_framework import viewsets, generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .oauth import OAuth42, oauth_42_instance
from .serializers import UserSerializer, PublicUserSerializer
from .serializers import UserUpdateSerializer, UserRegisterSerializer
from .permissions import IsSelfOrReadOnly
from .models import User

from .utils import generate_response_with_token, JWTAuthentication, generate_redirection_with_token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSelfOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PublicUserSerializer
        return UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_200_OK)

        user = serializer.save()
        return generate_response_with_token(user, 150000)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'success': False}, status=status.HTTP_200_OK)

        return generate_response_with_token(user, 150000)


@require_GET
def oauth_42(request):
    user = oauth_42_instance.get_user(request.GET.get('code'))
    return generate_redirection_with_token(user, 150000)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({'success': True})
        response.delete_cookie('access_token')
        return response


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({'success': False}, status=status.HTTP_200_OK)

        serializer.save()
        return Response({'success': True}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
