import logging
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Categoria, Producto
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    ProductoCreateSerializer,
)

# Configurar logger
logger = logging.getLogger('api')


@api_view(['GET'])
@permission_classes([AllowAny])
def api_home(request):
    """Página de inicio de la API"""
    logger.info("Acceso a la página de inicio de la API")
    return Response({
        'mensaje': 'Bienvenido a la API de Comida al Paso',
        'version': '1.0.0',
        'endpoints_disponibles': [
            'GET  /api/ - Información de la API',
            'GET  /api/test - Endpoint de prueba',
            'POST /api/token/ - Obtener token JWT',
            'POST /api/token/refresh/ - Refrescar token JWT',
            'POST /api/register/ - Registrar nuevo usuario',
            'GET  /api/categorias/ - Obtener todas las categorías',
            'POST /api/categorias/ - Crear nueva categoría (requiere autenticación)',
            'GET  /api/productos/ - Obtener todos los productos',
            'POST /api/productos/ - Crear nuevo producto (requiere autenticación)',
            'GET  /api/productos/<categoria> - Productos por categoría'
        ],
        'documentacion': 'Envía requests a los endpoints para interactuar con el inventario'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def test_api(request):
    """Endpoint de prueba"""
    logger.info("Test de API ejecutado")
    total_categorias = Categoria.objects.count()
    total_productos = Producto.objects.count()
    return Response({
        'mensaje': 'API funcionando correctamente',
        'total_categorias': total_categorias,
        'total_productos': total_productos
    })


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Intento de crear categoría por usuario: {request.user}")
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion', '')

        if not nombre:
            logger.warning("Intento de crear categoría sin nombre")
            return Response(
                {'error': 'Nombre es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            categoria = Categoria.objects.create(
                nombre=nombre,
                descripcion=descripcion
            )
            serializer = self.get_serializer(categoria)
            logger.info(f"Categoría creada exitosamente: {nombre}")
            return Response({
                'mensaje': 'Categoría creada exitosamente',
                'categoria': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error al crear categoría: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def productos_list(request):
    """Listar todos los productos o crear uno nuevo"""

    # GET → abierto al público
    if request.method == 'GET':
        logger.info("Listado de productos solicitado")
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    # POST → requiere estar logueado
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {"error": "Autenticación requerida para crear productos"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        logger.info(f"Intento de crear producto por usuario: {request.user}")
        create_serializer = ProductoCreateSerializer(data=request.data)

        if not create_serializer.is_valid():
            logger.warning(
                f"Datos inválidos para crear producto: {create_serializer.errors}")
            return Response(
                create_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            producto = create_serializer.save()
            logger.info(f"Producto creado exitosamente: {producto.nombre}")

            return Response({
                'mensaje': 'Producto creado exitosamente',
                'producto': {
                    'nombre': producto.nombre,
                    'categoria': producto.categoria.nombre,
                    'precio': float(producto.precio),
                    'stock': producto.stock
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error al crear producto: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def productos_por_categoria(request, categoria_nombre):
    """Obtener productos de una categoría específica"""
    logger.info(f"Búsqueda de productos por categoría: {categoria_nombre}")
    productos = Producto.objects.filter(
        categoria__nombre__iexact=categoria_nombre
    )

    if not productos.exists():
        logger.warning(
            f"No se encontraron productos para la categoría: {categoria_nombre}")

    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Registrar un nuevo usuario"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        logger.warning("Intento de registro sin username o password")
        return Response(
            {'error': 'Username y password son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        logger.warning(
            f"Intento de registro con username existente: {username}")
        return Response(
            {'error': 'El username ya existe'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        logger.info(f"Usuario registrado exitosamente: {username}")
        return Response({
            'mensaje': 'Usuario creado exitosamente',
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error al registrar usuario: {str(e)}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
