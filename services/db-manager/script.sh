#!/usr/bin/env bash
set -e

HOST="${POSTGRES_HOST:-postgresql}"
DB="${POSTGRES_DB}"
SUPERUSER="${POSTGRES_USER}"
SUPERPASS="${POSTGRES_PASSWORD}"

export PGPASSWORD="$SUPERPASS"


until psql -h "$HOST" -U "$SUPERUSER" -d "$DB" -c '\q' >/dev/null 2>&1; do
  echo "⏳ Waiting for PostgreSQL on $HOST…"
  sleep 2
done
echo "PostgreSQL is ready."


psql -h "$HOST" -U "$SUPERUSER" -d "$DB" <<-EOCREATE
CREATE TABLE IF NOT EXISTS public.movies_movie (
  id    SERIAL PRIMARY KEY,
  title TEXT NOT NULL
);
EOCREATE


for TABLE in users_user movies_movie; do
  echo "⏳ Waiting for table public.$TABLE…"
  until psql -h "$HOST" -U "$SUPERUSER" -d "$DB" -tAc \
      "SELECT COUNT(*) FROM information_schema.tables \
       WHERE table_schema='public' AND table_name='$TABLE';" \
    | grep -q "^1$"; do
    sleep 2
  done
  echo "Table public.$TABLE exists."
done


psql -h "$HOST" -U "$SUPERUSER" -d "$DB" <<-EOSQL
-- Révoquer d'abord tous les droits directs
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM backend_user, backend_movies;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM backend_user, backend_movies;
REVOKE ALL ON SCHEMA public FROM backend_user, backend_movies;

-- Révoquer les privilèges par défaut
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  REVOKE ALL ON TABLES FROM backend_user, backend_movies;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  REVOKE ALL ON SEQUENCES FROM backend_user, backend_movies;

-- Attribuer les rôles
GRANT role_users TO backend_user;
GRANT role_movies TO backend_movies;

-- Configurer les permissions de base des rôles
GRANT USAGE ON SCHEMA public TO role_users, role_movies;

-- Permissions spécifiques pour users
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.users_user TO role_users;
REVOKE ALL ON TABLE public.users_user FROM role_movies;
GRANT USAGE ON SEQUENCE public.users_user_id_seq TO role_users;

-- Permissions spécifiques pour movies
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.movies_movie TO role_movies;
REVOKE ALL ON TABLE public.movies_movie FROM role_users;
GRANT USAGE ON SEQUENCE public.movies_movie_id_seq TO role_movies;

-- Révoquer CREATE sur le schéma public
REVOKE CREATE ON SCHEMA public FROM PUBLIC, backend_user, backend_movies;

-- Forcer la réinitialisation des connexions existantes
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE usename IN ('backend_user', 'backend_movies')
AND pid <> pg_backend_pid();
EOSQL

echo "Grants and revokes applied successfully."
