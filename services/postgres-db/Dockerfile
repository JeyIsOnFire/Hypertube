FROM postgres:17

RUN apt-get update &&  \ 
  apt-get -y install postgresql-17-cron && \ 
  apt-get clean \ 
  && rm -rf /var/lib/apt/lists/*

COPY ./init_pg_cron.sh /docker-entrypoint-initdb.d/002_init_pg_cron.sh
COPY ./init-roles.sh /docker-entrypoint-initdb.d/003_init-roles.sh

RUN chmod +x /docker-entrypoint-initdb.d/002_init_pg_cron.sh && \
  chmod +x /docker-entrypoint-initdb.d/003_init-roles.sh