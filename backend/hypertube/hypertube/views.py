import pandas as pd
import requests
from django.http import JsonResponse

def hello_backend(request):
    print(request)
    return JsonResponse({"message":"Le Backend"})

def displayRandomPoster(request):
    # Charger les 1000 premières lignes du fichier TSV
    df = pd.read_csv(
        'imdb_data/data/title.basics.tsv.gz',
        sep='\t',
        compression='gzip',
        low_memory=False,
        usecols=['tconst', 'primaryTitle'],
        nrows=9  # Charger uniquement les 1000 premières lignes
    )

    # Sélectionner 10 lignes aléatoires
    random_sample = df.sample(n=9)

    # Ajouter les URLs des posters
    api_key = 'f5ffda2e'
    posters = []
    for _, row in random_sample.iterrows():
        tconst = row['tconst']
        response = requests.get(f"http://www.omdbapi.com/?i={tconst}&apikey={api_key}")
        if response.status_code == 200:
            data = response.json()
            posters.append({
                'tconst': tconst,
                'title': row['primaryTitle'],
                'poster_url': data.get('Poster', 'N/A')
            })
        else:
            posters.append({
                'tconst': tconst,
                'title': row['primaryTitle'],
                'poster_url': 'N/A'
            })

    # Retourner la réponse JSON
    return JsonResponse(posters, safe=False)
