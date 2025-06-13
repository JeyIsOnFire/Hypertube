#!/usr/bin/env bash
set -e
export PGPASSWORD="$POSTGRES_PASSWORD"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
DO \$\$
BEGIN
  -- creating role groups
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='role_users') THEN
    CREATE ROLE role_users NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='role_movies') THEN
    CREATE ROLE role_movies NOLOGIN;
  END IF;

  -- create backend superusers
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='backend_user') THEN
    CREATE ROLE backend_user LOGIN PASSWORD '${BACKEND_USER_PASSWORD}';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='backend_movies') THEN
    CREATE ROLE backend_movies LOGIN PASSWORD '${BACKEND_MOVIES_PASSWORD}';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='backend_scraper') THEN
    CREATE ROLE backend_scraper LOGIN PASSWORD '${BACKEND_SCRAPER_PASSWORD}';
  END IF;
END
\$\$;

-- granting permissions on backend super-users
GRANT CREATE ON SCHEMA public TO backend_user, backend_movies, backend_scraper;
GRANT USAGE  ON SCHEMA public TO backend_user, backend_movies, backend_scraper;
GRANT USAGE  ON SCHEMA cron TO backend_user, backend_movies, backend_scraper;
GRANT USAGE  ON ALL SEQUENCES IN SCHEMA public TO backend_user, backend_movies, backend_scraper;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT USAGE ON SEQUENCES TO backend_user, backend_movies, backend_scraper;
EOSQL

echo "init-roles.sh terminated successfully."
