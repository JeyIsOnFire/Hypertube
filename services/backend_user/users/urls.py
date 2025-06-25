# services/backend_user/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('oauth_42/', views.oauth_42, name='oauth_42'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('update/', views.UserUpdateView.as_view(), name='update'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]
