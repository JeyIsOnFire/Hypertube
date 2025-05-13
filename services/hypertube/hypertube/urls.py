from django.urls import path, re_path
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(r'^(?P<lang_code>en|fr)/fetchMovieData/', views.fetch_movie_data),
    re_path(r'^(?P<lang_code>en|fr)/fetchPopularMovies/(?P<pageNum>\d+)/$', views.fetch_popular_movies),
    re_path(r'^(?P<lang_code>en|fr)/getMovieInfosById/(?P<id>\d+)/$', views.get_movie_infos_by_id),
]

