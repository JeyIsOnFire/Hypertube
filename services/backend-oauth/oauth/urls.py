# services/backend-user/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', UserViewSet)


urlpatterns = [
    path('connect_42/', connect42.as_view(), name='connect_42'),
    path('connect_github/', connectGithub.as_view(), name='connect_github'),
    path('', include(router.urls)),
]

