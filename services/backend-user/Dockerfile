# services/backend-user/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Rendre le script exécutable (si ce n’est pas déjà fait dans le host)
RUN chmod +x ./entrypoint.sh

# Définir le script d'entrée par défaut
ENTRYPOINT ["./entrypoint.sh"]

# Commande par défaut lancée par le script (Uvicorn)
CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "6000"]
