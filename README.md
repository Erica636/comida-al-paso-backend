Comida al Paso - API REST
API REST desarrollada con Django para gestionar productos de un negocio gastronómico. Incluye autenticación JWT, seguridad OWASP, logging y está completamente dockerizada.
🚀 Tecnologías

Python 3.11
Django 5.x
Django REST Framework
PostgreSQL
Docker & Docker Compose
JWT (SimpleJWT)

📋 Requisitos Previos

Docker y Docker Compose instalados
Git

🔧 Instalación y Configuración
1. Clonar el repositorio
bashgit clone [tu-repo]
cd comida_al_paso_project
2. Configurar variables de entorno
Copia el archivo .env.example a .env y ajusta los valores:
bashcp .env.example .env
Variables importantes:

SECRET_KEY: Clave secreta de Django (cambiar en producción)
DEBUG: False para producción
DB_PASSWORD: Contraseña de PostgreSQL
JWT_ACCESS_TOKEN_LIFETIME: Duración del token en minutos

3. Crear la carpeta de logs
bashmkdir -p logs
touch logs/.gitkeep
4. Levantar los servicios con Docker
bashdocker-compose up --build
5. Ejecutar migraciones
En otra terminal:
bashdocker-compose exec web python manage.py migrate
6. Cargar datos iniciales
bashdocker-compose exec web python manage.py load_menu
7. Crear superusuario
bashdocker-compose exec web python manage.py createsuperuser
🌐 Endpoints Principales
Autenticación (JWT)

POST /api/token/ - Obtener token de acceso

json  {
    "username": "tu_usuario",
    "password": "tu_contraseña"
  }

POST /api/token/refresh/ - Refrescar token
POST /api/token/verify/ - Verificar token

Productos (públicos)

GET /api/productos/ - Listar todos los productos
GET /api/productos/{categoria}/ - Productos por categoría

Categorías (públicas)

GET /api/categorias/ - Listar categorías

Endpoints Protegidos (requieren JWT)

POST /api/productos/ - Crear producto
POST /api/categorias/ - Crear categoría

Admin

/admin/ - Panel de administración de Django

🔐 Autenticación
Para usar endpoints protegidos, incluye el token en el header:
bashAuthorization: Bearer <tu-token>
Ejemplo con curl:
bashcurl -H "Authorization: Bearer tu_token_aqui" \
     http://localhost:8000/api/productos/
📊 Logging
Los logs se guardan en /logs/django.log con el siguiente formato:
[INFO] 2025-01-15 10:30:00 api views 1234 5678 - Producto creado exitosamente: Hamburguesa
Niveles de log configurables en .env:

DJANGO_LOG_LEVEL: INFO, DEBUG, WARNING, ERROR
API_LOG_LEVEL: DEBUG por defecto

🔒 Seguridad
Características implementadas:

✅ Autenticación JWT
✅ Variables sensibles en .env
✅ DEBUG=False en producción
✅ ALLOWED_HOSTS configurado
✅ CORS configurado
✅ Uso del ORM (sin SQL raw)
✅ Validaciones en serializers
✅ Logging completo
✅ Headers de seguridad (cuando DEBUG=False)

Headers de seguridad (producción):

SECURE_SSL_REDIRECT
SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE
SECURE_BROWSER_XSS_FILTER
SECURE_CONTENT_TYPE_NOSNIFF
X_FRAME_OPTIONS

🐳 Docker
Comandos útiles:
bash# Ver logs
docker-compose logs -f web

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ejecutar comando en el contenedor
docker-compose exec web python manage.py [comando]

# Ver base de datos
docker-compose exec db psql -U postgres -d comida_al_paso_db
📁 Estructura del Proyecto
comida_al_paso_project/
├── api/
│   ├── management/
│   │   └── commands/
│   │       └── load_menu.py
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── comida_al_paso/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── logs/
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
└── README.md
🧪 Testing
Para ejecutar tests:
bashdocker-compose exec web python manage.py test
🚢 Despliegue
Variables de entorno para producción:
DEBUG=False
SECRET_KEY=[generar-nueva-clave-segura]
ALLOWED_HOSTS=tudominio.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
Generar SECRET_KEY nueva:
bashpython -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
📝 Notas

El proyecto cumple con los requisitos de seguridad OWASP
Las contraseñas se validan con los validadores de Django
Los logs incluyen timestamp, level, logger y mensaje
CORS está configurado para desarrollo local

👤 Autor
Erica Ansaloni

¿Problemas? Revisa los logs en /logs/django.log o los logs de Docker con docker-compose logs -f web
## Deploy en Railway
Proyecto deployado en Railway con MySQL.
