#!/bin/bash

set -e

CONTAINER_NAME="${1:-mongo-blog}"
DB_NAME="blog_db"

echo "Vérification du conteneur : $CONTAINER_NAME"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "ERREUR : le conteneur '$CONTAINER_NAME' n'est pas en cours d'exécution."
  exit 1
fi

echo "1) Vérification de l'utilisateur interne..."
CURRENT_USER=$(docker exec "$CONTAINER_NAME" whoami 2>/dev/null || true)

if [ -z "$CURRENT_USER" ]; then
  echo "ERREUR : impossible d'exécuter 'whoami' dans le conteneur."
  exit 1
fi

if [ "$CURRENT_USER" = "root" ]; then
  echo "ERREUR : MongoDB s'exécute en root, ce qui n'est pas autorisé."
  exit 1
fi

echo "OK : utilisateur interne = $CURRENT_USER"

echo "2) Vérification de la base et de la collection..."
POST_COUNT=$(docker exec "$CONTAINER_NAME" mongosh --quiet \
  -u "$MONGO_INITDB_ROOT_USERNAME" \
  -p "$MONGO_INITDB_ROOT_PASSWORD" \
  --authenticationDatabase admin \
  --eval "db.getSiblingDB('$DB_NAME').posts.countDocuments()")

if [ -z "$POST_COUNT" ]; then
  echo "ERREUR : impossible d'interroger MongoDB."
  exit 1
fi

echo "OK : blog_db répond et posts contient $POST_COUNT documents."

echo "SUCCÈS : tous les contrôles sont validés."