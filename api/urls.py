from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', views.api_home, name='api-home'),
    path('test/', views.test_api, name='test-api'),

    # JWT AUTHENTICATION
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.register, name='register'),
    # Rutas de Django REST Framework
    path('', include(router.urls)),

    # PRODUCTOS
    path('productos/', views.productos_list, name='productos-list'),
    path('productos/<str:categoria_nombre>/',
         views.productos_por_categoria, name='productos-por-categoria'),
]
