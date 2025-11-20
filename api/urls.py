from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', views.api_home, name='api-home'),
    path('test/', views.test_api, name='test-api'),

    # Rutas de Django REST Framework
    path('', include(router.urls)),

    # PRODUCTOS
    path('productos/', views.productos_list, name='productos-list'),
    path('productos/<str:categoria_nombre>/', views.productos_por_categoria, name='productos-por-categoria'),
]
