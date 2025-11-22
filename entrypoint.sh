#!/bin/bash

set -e

echo "============================================"
echo "Iniciando Comida al Paso - Backend"
echo "============================================"

echo "Esperando a que la base de datos este disponible..."
sleep 3

echo "Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

echo "Recolectando archivos estaticos..."
python manage.py collectstatic --noinput

echo "============================================"
echo "Iniciando servidor Gunicorn..."
echo "============================================"

exec "$@"