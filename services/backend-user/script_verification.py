# django_shell.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django.db import connection
from django.apps import apps

print("✅ Environnement Django initialisé.")
print("📦 Tables dans la base de données :")
for table in connection.introspection.table_names():
    print("-", table)

print("\n📦 Modèles enregistrés dans l'app 'users' :")
for model in apps.get_app_config('users').get_models():
    print("-", model.__name__)
