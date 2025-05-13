import os
import pandas as pd
import requests
import random
import logging
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_language
from django.db import connection
from dotenv import load_dotenv

import re

load_dotenv()

def tmdb_auth():
    api_key = os.getenv("TMDB_API_KEY")
    token = os.getenv("TMDB_TOKEN")
    auth_url = "https://api.themoviedb.org/3/authentication"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
    }
    auth_response = requests.get(auth_url, headers=headers)
    if auth_response.status_code != 200:
        return JsonResponse({'error': 'Authentication failed'}, status=auth_response.status_code)
    return headers

def fetch_with_scraper(request, movie_data):
        filtered_movies = {
            'results': []
        }
        scraper_url = f"http://scraper:8000/search?query="
        formatted_for_scrap = []
        for movie in movie_data['results']:
            movie_name = movie['original_title']
            movie_year = movie['release_date'][:4]
            if movie_name:
                formatted_for_scrap.append(movie_name + " " + str(movie_year))
        scrapper_response = requests.get(scraper_url + ",".join(formatted_for_scrap))
        if scrapper_response.status_code == 200:
            scrap_data = scrapper_response.json()
            for movie in movie_data['results']:
                movie_keyword = movie['original_title'] + " " + str(movie['release_date'][:4])
                if movie_keyword in scrap_data:
                    original_title = re.sub(r'[._\-]+', ' ', movie["original_title"].lower())
                    original_title = re.sub(':', '', original_title)
                    if original_title in scrap_data[movie_keyword]:
                        filtered_movies['results'].append(movie)
        return filtered_movies

def fetch_movie_data(request, lang_code='fr'):
    headers = tmdb_auth()
    movie_url = f"https://api.themoviedb.org/3/search/movie?query={request.GET.get('query', '')}&language={lang_code}&page=1"
    movie_response = requests.get(movie_url, headers=headers)
    if movie_response.status_code == 200:
        movie_data = movie_response.json() 
        filtered_movies = fetch_with_scraper(request, movie_data)
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movie_response.status_code)
    return JsonResponse(filtered_movies, safe=False)


def fetch_popular_movies(request, lang_code='fr', pageNum=None):
    headers = tmdb_auth()
    movies_url = f"https://api.themoviedb.org/3/movie/popular?language={lang_code}&page={pageNum}"
    movies_response = requests.get(movies_url, headers=headers)
    if movies_response.status_code == 200:
        movies_data = movies_response.json()
        filtered = fetch_with_scraper(request, movies_data)
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movies_response.status_code)
    return JsonResponse(filtered, safe=False)


def get_movie_infos_by_id(request, lang_code='fr', id=None):
    headers = tmdb_auth()
    movie_url = f"https://api.themoviedb.org/3/movie/{id}?language={lang_code}&page=1"
    credits_url = f"https://api.themoviedb.org/3/movie/{id}/credits?language={lang_code}&page=1"
    movie_response = requests.get(movie_url, headers=headers)
    credits_response = requests.get(credits_url, headers=headers)
    if movie_response.status_code == 200 and credits_response.status_code == 200:
        movie_data = movie_response.json()
        credits_data = credits_response.json()
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movie_response.status_code)
    return JsonResponse({"movie_data": movie_data, "credits_data": credits_data}, safe=False)
