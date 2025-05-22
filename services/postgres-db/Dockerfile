FROM postgres:17-alpine

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY init-roles.sh /docker-entrypoint-initdb.d/init-roles.sh

RUN chmod +x /docker-entrypoint-initdb.d/init-roles.sh
