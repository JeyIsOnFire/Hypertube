from django.urls import path, re_path
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(r'^(?P<lang_code>en|fr)/hello/', views.hello_backend),
    re_path(r'^(?P<lang_code>en|fr)/randomPoster/', views.display_random_poster),
    re_path(r'^(?P<lang_code>en|fr)/displayQuery/', views.display_query),
]

