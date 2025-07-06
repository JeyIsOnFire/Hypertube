# backend/Dockerfile

# Étape 1 : Utiliser l'image officielle de Python
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail à l'intérieur du container
WORKDIR /app
COPY . .

# Étape 3 : Copier les fichiers requirements.txt et installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

# Étape 4 : Copier tout le code source dans le container

# Étape 5 : Exposer le port 8000 pour Django
EXPOSE 7000

# Étape 6 : Lancer le serveur Django (en mode de développement)
CMD ["uvicorn", "hypertube.asgi:application", "--host", "0.0.0.0", "--port", "7000", "--reload"]

