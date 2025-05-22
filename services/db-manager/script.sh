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
GRANT role_users  TO backend_user;
GRANT role_movies TO backend_movies;

GRANT USAGE ON SCHEMA public TO role_users, role_movies;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.users_user TO role_users;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.movies_movie TO role_movies;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_users, role_movies;

REVOKE CREATE ON SCHEMA public FROM PUBLIC, backend_user, backend_movies;    
EOSQL

echo "Grants applied successfully."
