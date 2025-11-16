#!/bin/bash

set -e

echo "Iniciando aplicación Comida al Paso API"

# Ejecutar migraciones
echo "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Cargar datos iniciales si la base está vacía
echo "Verificando datos iniciales..."
python manage.py load_menu_data || echo "Datos ya cargados o comando no disponible"

echo "Aplicación preparada exitosamente"

# Determinar modo de ejecución según ENV
if [ "$ENV" = "production" ]; then
    echo "Iniciando en modo PRODUCCIÓN con GUNICORN..."
    exec gunicorn comida_al_paso.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -
else
    echo "Iniciando en modo DESARROLLO con runserver..."
    exec python manage.py runserver 0.0.0.0:8000
fi
