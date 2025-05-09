import os
import pandas as pd
import requests
import random
import logging
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_language
from django.db import connection
from dotenv import load_dotenv

load_dotenv();

def tmdb_auth():
    api_key = os.getenv("TMDB_API_KEY");
    token = os.getenv("TMDB_TOKEN");
    auth_url = "https://api.themoviedb.org/3/authentication"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
    }
    auth_response = requests.get(auth_url, headers=headers)
    if auth_response.status_code != 200:
        return JsonResponse({'error': 'Authentication failed'}, status=auth_response.status_code)
    return headers


def fetch_movie_data(request, lang_code='en'):
    headers = tmdb_auth()
    movie_url = f"https://api.themoviedb.org/3/search/movie?query={request.GET.get('query', '')}&language={lang_code}&page=1"
    movie_response = requests.get(movie_url, headers=headers)
    if movie_response.status_code == 200:
        movie_data = movie_response.json() 
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movie_response.status_code)
    return JsonResponse(movie_data, safe=False)


def fetch_popular_movies(request, lang_code='en', pageNum=None):
    headers = tmdb_auth()
    movies_url = f"https://api.themoviedb.org/3/movie/popular?language={lang_code}&page={pageNum}"
    movies_response = requests.get(movies_url, headers=headers)
    if movies_response.status_code == 200:
        movies_data = movies_response.json()
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movies_response.status_code)
    return JsonResponse(movies_data, safe=False)


def get_movie_infos_by_id(request, lang_code='en', id=None):
    headers = tmdb_auth()
    movie_url = f"https://api.themoviedb.org/3/movie/{id}?language={lang_code}&page=1"
    movie_response = requests.get(movie_url, headers=headers)
    if movie_response.status_code == 200:
        movie_data = movie_response.json()
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movie_response.status_code)
    return JsonResponse(movie_data, safe=False)
