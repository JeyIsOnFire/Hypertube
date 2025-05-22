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

DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_users') THEN
    CREATE ROLE role_users NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_movies') THEN
    CREATE ROLE role_movies NOLOGIN;
  END IF;
END
\$\$;


GRANT USAGE ON SCHEMA public TO role_users;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.users_user TO role_users;

GRANT USAGE ON SCHEMA public TO role_movies;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.movies_movie TO role_movies;


DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${BACKEND_USER_NAME}') THEN
    CREATE USER "${BACKEND_USER_NAME}" WITH ENCRYPTED PASSWORD '${BACKEND_USER_PASSWORD}';
    GRANT role_users TO "${BACKEND_USER_NAME}";
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${BACKEND_MOVIES_NAME}') THEN
    CREATE USER "${BACKEND_MOVIES_NAME}" WITH ENCRYPTED PASSWORD '${BACKEND_MOVIES_PASSWORD}';
    GRANT role_movies TO "${BACKEND_MOVIES_NAME}";
  END IF;
END
\$\$;


ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_users, role_movies;
EOSQL

echo "Grants applied successfully."
