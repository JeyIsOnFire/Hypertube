# services/backend_user/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, UserUpdateView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView


router = DefaultRouter()
router.register(r'', UserViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/',  TokenVerifyView.as_view(),  name='token_verify'),
    path('', include(router.urls)),
]
