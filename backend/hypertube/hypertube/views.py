import pandas as pd
import requests
import random
import logging
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_language
from django.db import connection

def omdb_auth():
    api_key = "f79480e4f43a3fae72de354de3e27a0d"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzk0ODBlNGY0M2EzZmFlNzJkZTM1NGRlM2UyN2EwZCIsIm5iZiI6MTc0NjUzOTc5NS4yNjksInN1YiI6IjY4MWExNTEzZDA1YjI1MTI4Y2M2MzU1MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FnkH26lSSBoFw_slKP6VGU0HxrnPf0Z_V--Kr0Oe9y8"
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
    headers = omdb_auth()
    movie_url = f"https://api.themoviedb.org/3/search/movie?query={request.GET.get('query', '')}&language={lang_code}&page=1"
    movie_response = requests.get(movie_url, headers=headers)
    if movie_response.status_code == 200:
        movie_data = movie_response.json() 
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movie_response.status_code)
    return JsonResponse(movie_data, safe=False)


def fetch_popular_movies(request, lang_code='en'):
    headers = omdb_auth()
    movies_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    movies_response = requests.get(movies_url, headers=headers)
    if movies_response.status_code == 200:
        movies_data = movies_response.json()
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movies_response.status_code)
    return JsonResponse(movies_data, safe=False)


