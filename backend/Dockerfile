# backend/Dockerfile

# Étape 1 : Utiliser l'image officielle de Python
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail à l'intérieur du container
WORKDIR /app

# Étape 3 : Copier les fichiers requirements.txt et installer les dépendances
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

# Étape 4 : Copier tout le code source dans le container
COPY backend/hypertube /app/

# Étape 5 : Exposer le port 8000 pour Django
EXPOSE 5000

# Étape 6 : Lancer le serveur Django (en mode de développement)
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]

