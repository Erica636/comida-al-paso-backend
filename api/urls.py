from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', views.api_home, name='api-home'),
    path('test/', views.test_api, name='test-api'),

    # Categorías (router)
    path('', include(router.urls)),

    # Productos (GET público, POST/PUT/DELETE con token)
    path('productos/', views.productos_list, name='productos-list'),

    # Productos por categoría (IMPORTANTE: barra al final)
    re_path(r'^productos/(?P<categoria_nombre>[^/]+)/$', views.productos_por_categoria,
            name='productos-por-categoria'),
]
