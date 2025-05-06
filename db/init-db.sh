#!/bin/bash
set -e

echo "Téléchargement du dump..."
curl -L "https://www.dropbox.com/scl/fi/4m90csmkbbwscsw3qqjoh/sauvegarde.dump?rlkey=ac7zhll5q8cnawekgvdmh0djq&st=7xd1mudo&dl=1" -o /tmp/dump

echo "Restauration du dump..."
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" /tmp/dump

