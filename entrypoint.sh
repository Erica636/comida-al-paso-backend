#!/bin/bash

set -e

echo "============================================"
echo "Iniciando Comida al Paso - Backend"
echo "============================================"

echo "Esperando a que la base de datos este disponible..."
sleep 3

echo "Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

echo "Creando superusuario si no existe..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuario creado: admin / admin123')
else:
    print('Superusuario ya existe')
END

echo "Cargando datos iniciales si la base esta vacia..."
python manage.py shell << END
from api.models import Producto
if Producto.objects.count() == 0:
    import os
    os.system('python manage.py loaddata fixtures/productos_inicial.json')
    print('Datos iniciales cargados')
else:
    print('Ya existen productos en la base')
END

echo "Recolectando archivos estaticos..."
python manage.py collectstatic --noinput

echo "============================================"
echo "Iniciando servidor Gunicorn..."
echo "============================================"

exec "$@"