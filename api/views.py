from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer
from .permissions import IsAdminUser


# ========== AUTENTICACIÓN ==========

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registrar nuevo usuario
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username y password son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'El usuario ya existe'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response(
        {'message': 'Usuario creado exitosamente', 'username': user.username},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    Obtener información del usuario autenticado
    """
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff
    })


# ========== PRODUCTOS ==========

class StandardPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([AllowAny])
def listar_productos(request):
    """
    Listar todos los productos (público)
    """
    productos = Producto.objects.all()
    paginator = StandardPagination()
    paginated = paginator.paginate_queryset(productos, request)
    serializer = ProductoSerializer(paginated, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def crear_producto(request):
    """
    Crear nuevo producto (solo admin)
    """
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def actualizar_producto(request, pk):
    """
    Actualizar producto existente (solo admin)
    """
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def eliminar_producto(request, pk):
    """
    Eliminar producto (solo admin)
    """
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )

    nombre = producto.nombre
    producto.delete()
    return Response(
        {'message': f'Producto "{nombre}" eliminado correctamente'},
        status=status.HTTP_200_OK
    )


# ========== CATEGORÍAS ==========

@api_view(['GET'])
@permission_classes([AllowAny])
def listar_categorias(request):
    """
    Listar todas las categorías (público)
    """
    categorias = Categoria.objects.all()
    paginator = StandardPagination()
    paginated = paginator.paginate_queryset(categorias, request)
    serializer = CategoriaSerializer(paginated, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def crear_categoria(request):
    """
    Crear nueva categoría (solo admin)
    """
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== COMPRAS ==========

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def procesar_compra(request):
    """
    Procesar compra y descontar stock
    """
    items = request.data.get('items', [])

    if not items:
        return Response(
            {'error': 'El carrito está vacío'},
            status=status.HTTP_400_BAD_REQUEST
        )

    errores = []
    productos_actualizados = []

    # Verificar stock disponible
    for item in items:
        try:
            producto = Producto.objects.get(pk=item['id'])
            if producto.stock < item['cantidad']:
                errores.append(
                    f'{producto.nombre}: stock insuficiente (disponible: {producto.stock})')
            else:
                productos_actualizados.append({
                    'producto': producto,
                    'cantidad': item['cantidad']
                })
        except Producto.DoesNotExist:
            errores.append(f'Producto ID {item["id"]} no encontrado')

    if errores:
        return Response(
            {'error': 'No se pudo procesar la compra', 'detalles': errores},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Descontar stock
    for item in productos_actualizados:
        producto = item['producto']
        producto.stock -= item['cantidad']
        producto.save()

    return Response({
        'message': 'Compra realizada exitosamente',
        'productos': len(productos_actualizados)
    }, status=status.HTTP_200_OK)
