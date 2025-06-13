#!/bin/bash

cat <<EOF >> /var/lib/postgresql/data/postgresql.conf
# Enable pg_cron extension
shared_preload_libraries = 'pg_cron'
# pg_cron configuration
cron.database_name = 'hypertube-db'
# Set the timezone for pg_cron
cron.timezone = 'Europe/Paris'
EOF

pg_ctl restart

# Wait for PostgreSQL to restart
until pg_isready -d hypertube-db; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Create the pg_cron extension in the hypertube-db database
psql -d hypertube-db -U ${POSTGRES_USER} -c "CREATE EXTENSION IF NOT EXISTS pg_cron;"