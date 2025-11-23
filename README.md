# Comida al Paso - Backend API

API REST desarrollada con Django y Django REST Framework para gestionar productos de un negocio gastronómico con autenticación JWT.

## Tecnologías

- Python 3.12
- Django 4.2
- Django REST Framework
- djangorestframework-simplejwt
- django-cors-headers
- PostgreSQL (Docker) / SQLite (desarrollo local)
- Gunicorn
- Docker & Docker Compose

## Estructura del Proyecto
```
backend/
├── api/
│   ├── management/
│   │   └── commands/
│   │       ├── init.py
│   │       └── load_menu_data.py
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── comida_al_paso/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── fixtures/
│   └── initial_data.json
├── logs/
│   └── django.log
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
└── requirements.txt
```

## Instalación

### Opción 1: Docker (recomendado)

1. Clonar el repositorio y entrar a la carpeta backend:
```bash
cd backend
```

2. Copiar el archivo de variables de entorno:
```bash
cp .env.example .env
```

3. Construir y levantar los contenedores:
```bash
docker-compose up --build
```

4. (Opcional) Crear superusuario:
```bash
docker-compose exec web python manage.py createsuperuser
```

La API estará disponible en: http://localhost:8000/api/

### Opción 2: Desarrollo Local (sin Docker)

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno virtual:
   - Windows PowerShell: `.\venv\Scripts\Activate.ps1`
   - Windows CMD: `.\venv\Scripts\Activate`
   - Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Copiar variables de entorno:
```bash
cp .env.example .env
```

5. Ajustar `.env` para desarrollo local:
```
DB_ENGINE=sqlite
DEBUG=True
```

6. Ejecutar migraciones:
```bash
python manage.py migrate
```

7. Crear superusuario:
```bash
python manage.py createsuperuser
```

8. Iniciar servidor:
```bash
python manage.py runserver
```

## Modelos

### Categoria

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Identificador único |
| nombre | CharField(100) | Nombre único de la categoría |
| descripcion | TextField | Descripción opcional |

### Producto

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BigAutoField | Identificador único |
| nombre | CharField(200) | Nombre del producto |
| descripcion | TextField | Descripción opcional |
| precio | DecimalField | Precio con 2 decimales |
| categoria | ForeignKey | Relación con Categoria |
| stock | IntegerField | Cantidad disponible |
| disponible | BooleanField | Estado de disponibilidad |
| created_at | DateTimeField | Fecha de creación |

## Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | /api/register/ | Registrar nuevo usuario | No |
| POST | /api/token/ | Obtener token JWT (login) | No |
| POST | /api/token/refresh/ | Refrescar token | No |
| GET | /api/user/ | Info del usuario autenticado | Sí |

### Productos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | /api/productos/ | Listar productos (paginado) | No |
| POST | /api/productos/crear/ | Crear producto | Admin |
| PUT | /api/productos/{id}/ | Actualizar producto | Admin |
| DELETE | /api/productos/{id}/eliminar/ | Eliminar producto | Admin |

### Categorías

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | /api/categorias/ | Listar categorías (paginado) | No |
| POST | /api/categorias/crear/ | Crear categoría | Admin |

### Compras

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | /api/comprar/ | Procesar compra y descontar stock | Sí |

## Sistema de Roles

### Usuario Normal (is_staff=False)
- Ver productos y categorías
- Agregar productos al carrito
- Procesar compras

### Administrador (is_staff=True)
- Todo lo anterior
- Crear, editar y eliminar productos
- Crear categorías
- Acceso al panel de administración

## Autenticación JWT

Para usar endpoints protegidos, incluir el token en el header:
```
Authorization: Bearer {access_token}
```

### Ejemplo: Obtener token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"tu_usuario","password":"tu_password"}'
```

### Ejemplo: Usar token en petición
```bash
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/user/
```

## Demo Guiada

### 1. Login
```bash
# Obtener token JWT
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"tu_usuario","password":"tu_password"}'

# Respuesta exitosa:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
}
```

### 2. CRUD de Productos

**Listar productos (público):**
```bash
curl http://localhost:8000/api/productos/
```

**Crear producto (admin):**
```bash
curl -X POST http://localhost:8000/api/productos/crear/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Pizza Napolitana","categoria":10,"precio":4500,"stock":15}'
```

**Actualizar producto (admin):**
```bash
curl -X PUT http://localhost:8000/api/productos/1/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"precio":4800}'
```

**Eliminar producto (admin):**
```bash
curl -X DELETE http://localhost:8000/api/productos/1/eliminar/ \
  -H "Authorization: Bearer {token}"
```

### 3. Manejo de Errores

**Error de validación (precio negativo):**
```bash
curl -X POST http://localhost:8000/api/productos/crear/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","categoria":9,"precio":-100,"stock":10}'

# Respuesta:
{
  "precio": ["El precio debe ser mayor a 0."]
}
```

**Error de autenticación:**
```bash
curl -X POST http://localhost:8000/api/productos/crear/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","categoria":9,"precio":1000,"stock":10}'

# Respuesta:
{
  "detail": "Authentication credentials were not provided."
}
```

**Error de permisos (usuario no admin):**
```bash
# Respuesta:
{
  "detail": "No tiene permiso para realizar esta acción."
}
```

### 4. Caso Borde: Stock Insuficiente
```bash
curl -X POST http://localhost:8000/api/comprar/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"id":1,"cantidad":9999}]}'

# Respuesta:
{
  "error": "No se pudo procesar la compra",
  "detalles": ["Hamburguesa Clásica: stock insuficiente (disponible: 18)"]
}
```

## Configuración de Seguridad

### Variables de Entorno

El proyecto usa variables de entorno para configuración sensible. Ver `.env.example` para referencia.

| Variable | Descripción | Default |
|----------|-------------|---------|
| SECRET_KEY | Clave secreta de Django | (requerido en prod) |
| DEBUG | Modo debug | False |
| ALLOWED_HOSTS | Hosts permitidos | localhost,127.0.0.1 |
| DB_ENGINE | Motor de BD (postgres/mysql/sqlite) | sqlite |
| POSTGRES_* | Configuración PostgreSQL | - |

### Seguridad en Producción

Cuando `DEBUG=False`, se activan automáticamente:
- SESSION_COOKIE_SECURE
- CSRF_COOKIE_SECURE
- SECURE_BROWSER_XSS_FILTER
- SECURE_CONTENT_TYPE_NOSNIFF
- X_FRAME_OPTIONS = DENY

## Arquitectura y Decisiones Técnicas

### ¿Por qué Django REST Framework?
- Serializers robustos con validaciones integradas
- Sistema de permisos flexible
- Paginación automática
- Documentación automática de API

### ¿Por qué JWT?
- Stateless: no requiere sesiones en servidor
- Escalable: funciona con múltiples instancias
- Seguro: tokens firmados y con expiración

### ¿Por qué PostgreSQL en Docker?
- Base de datos robusta para producción
- Consistencia entre desarrollo y producción
- Fácil de escalar y respaldar

### Separación de Capas
```
api/
├── models.py      → Capa de datos (ORM)
├── serializers.py → Capa de validación/transformación
├── views.py       → Capa de lógica de negocio
├── permissions.py → Capa de autorización
└── urls.py        → Capa de ruteo
```

## Logging

El sistema registra eventos en consola con formato:
```
[LEVEL] timestamp logger - message
```

Niveles configurables via `.env`:
- DJANGO_LOG_LEVEL (default: INFO)
- API_LOG_LEVEL (default: DEBUG)

## Mejoras Futuras

- Implementar tests unitarios y de integración
- Agregar documentación Swagger/OpenAPI
- Implementar caché con Redis
- Agregar sistema de pedidos con historial
- Implementar búsqueda y filtros avanzados
- Agregar imágenes a productos
- Implementar sistema de valoraciones

## Crear Superusuario

Para acceder al panel de administración en Railway, el superusuario se crea automáticamente al desplegar.

Para desarrollo local:
```bash
python manage.py createsuperuser
```

Seguí las instrucciones en la terminal para crear tu usuario administrador.

## Licencia

Este proyecto es de uso educativo.

---

Desarrollado por Erica R. Ansaloni - 2025