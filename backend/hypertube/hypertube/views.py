import pandas as pd
import requests
import random
import logging
from django.http import JsonResponse, HttpResponse
from django.utils.translation import get_language
from django.db import connection

def hello_backend(request):
    print(request)
    return JsonResponse({"message":"Le Backend"})

def display_random_poster(request, lang_code='en'):
    # Sélectionner 9 titres aléatoires depuis la base de données
    with connection.cursor() as cursor:
        cursor.execute("SELECT tconst, primary_title FROM titles ORDER BY RANDOM() LIMIT 9;")
        random_titles = cursor.fetchall()

    # Appel à l’API OMDb pour obtenir les posters
    api_key = 'f5ffda2e'
    posters = []
    for tconst, title in random_titles:
        response = requests.get(f"http://www.omdbapi.com/?i={tconst}&apikey={api_key}")
        if response.status_code == 200:
            data = response.json()
            poster_url = data.get('Poster', 'N/A')
        else:
            poster_url = 'N/A'

        posters.append({
            'tconst': tconst,
            'title': title,
            'poster_url': poster_url
        })

    return JsonResponse(posters, safe=False)

def display_query(request, lang_code = get_language()):
    query = request.GET.get('query', '')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM titles WHERE primary_title LIKE %s LIMIT 10;", [f"%{query}%"])
        result = cursor.fetchall();
    
    return JsonResponse({'received_query': result})

def fetch_movie_data(request, lang_code='en'):
    api_key = "f79480e4f43a3fae72de354de3e27a0d"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzk0ODBlNGY0M2EzZmFlNzJkZTM1NGRlM2UyN2EwZCIsIm5iZiI6MTc0NjUzOTc5NS4yNjksInN1YiI6IjY4MWExNTEzZDA1YjI1MTI4Y2M2MzU1MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FnkH26lSSBoFw_slKP6VGU0HxrnPf0Z_V--Kr0Oe9y8"

    # 1ère requête : Authentification
    auth_url = "https://api.themoviedb.org/3/authentication"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
    }
    auth_response = requests.get(auth_url, headers=headers)

    if auth_response.status_code != 200:
        return JsonResponse({'error': 'Authentication failed'}, status=auth_response.status_code)


    # 2ème requête : Récupérer les films
    log = logging.getLogger('django')

    movie_url = f"https://api.themoviedb.org/3/search/movie?query={request.GET.get('query', '')}&language={lang_code}&page=1"

    movie_response = requests.get(movie_url, headers=headers)

    if movie_response.status_code == 200:
        movie_data = movie_response.json()  # Extraire le JSON de la réponse
    else:
        return JsonResponse({'error': 'Failed to fetch movie data'}, status=movie_response.status_code)

    # Retourner la réponse avec les données des films
    return JsonResponse(movie_data, safe=False)




