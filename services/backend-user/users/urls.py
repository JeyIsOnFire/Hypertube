# services/backend-user/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, UserUpdateView, ProfileView


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', ShowUsersList.as_view(), name='users')
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
