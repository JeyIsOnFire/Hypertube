#!/usr/bin/env bash
set -e

apt-get update
apt-get install -y curl

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

$res = $(curl "http://backend-scraper:8000/health" -o /dev/null)
echo $res
until [[ $res == *"200 OK"* ]]; do
  echo "⏳ Waiting for backend-scraper…"
  sleep 2
  $res = $(curl "http://backend-scraper:8000/health" -o /dev/null)
done

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
GRANT role_movies TO backend_scraper;

GRANT USAGE ON SCHEMA public TO role_users, role_movies;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.users_user TO role_users;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.movies_movie TO role_movies;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_users, role_movies;

REVOKE CREATE ON SCHEMA public FROM PUBLIC, backend_user, backend_movies, backend_scraper;
REVOKE USAGE  ON SCHEMA cron TO backend_user, backend_movies, backend_scraper;
EOSQL

echo "Grants applied successfully."
