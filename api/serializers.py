from rest_framework import serializers
from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                'El nombre de la categoría es obligatorio.')
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                'El nombre debe tener al menos 2 caracteres.')
        return value.strip()


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'categoria_nombre',
                  'precio', 'stock', 'descripcion', 'disponible']

    def get_categoria_nombre(self, obj):
        if obj.categoria:
            return obj.categoria.nombre
        return None

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                'El nombre del producto es obligatorio.')
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                'El nombre debe tener al menos 2 caracteres.')
        return value.strip()

    def validate_precio(self, value):
        if value is None:
            raise serializers.ValidationError('El precio es obligatorio.')
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor a 0.')
        return value

    def validate_stock(self, value):
        if value is None:
            raise serializers.ValidationError('El stock es obligatorio.')
        if value < 0:
            raise serializers.ValidationError(
                'El stock no puede ser negativo.')
        return value

    def validate_categoria(self, value):
        if not value:
            raise serializers.ValidationError(
                'Debe seleccionar una categoría.')
        return value
