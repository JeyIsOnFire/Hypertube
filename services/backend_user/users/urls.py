# services/backend_user/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, UserUpdateView, ProfileView, LoginView, LogoutView, ConnectOAuthView

router = DefaultRouter()
router.register(r'', UserViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('connect-oauth/', ConnectOAuthView.as_view(), name='connect-oauth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]
