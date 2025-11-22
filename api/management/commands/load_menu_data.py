from django.core.management.base import BaseCommand
from api.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Carga los datos iniciales del menú del restaurante'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos del menú...')

        # Limpiar datos existentes
        Producto.objects.all().delete()
        Categoria.objects.all().delete()
        self.stdout.write(self.style.WARNING('Datos anteriores eliminados'))

        # Crear categorías
        categorias_data = [
            ("Hamburguesas", "Hamburguesas clásicas y gourmet"),
            ("Pizzas", "Pizzas artesanales con ingredientes frescos"),
            ("Empanadas", "Empanadas caseras rellenas"),
            ("Parrilla", "Carnes a la parrilla y choripán"),
            ("Pastas", "Pastas frescas y salsas caseras"),
            ("Ensaladas", "Ensaladas frescas y saludables"),
            ("Bebidas", "Bebidas frías y calientes"),
            ("Postres", "Postres caseros y helados"),
        ]

        categorias = {}
        for nombre, descripcion in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion}
            )
            categorias[nombre] = categoria
            if created:
                self.stdout.write(f'  Categoria creada: {nombre}')

        # Crear productos
        productos_data = [
            # Hamburguesas (12)
            ("Hamburguesa Clasica", "Hamburguesas", 2500, 20),
            ("Hamburguesa Completa", "Hamburguesas", 3200, 15),
            ("Hamburguesa BBQ", "Hamburguesas", 3500, 12),
            ("Hamburguesa Doble Carne", "Hamburguesas", 4200, 10),
            ("Hamburguesa con Bacon", "Hamburguesas", 3800, 14),
            ("Hamburguesa Criolla", "Hamburguesas", 3400, 11),
            ("Hamburguesa Veggie", "Hamburguesas", 3000, 8),
            ("Hamburguesa de Pollo", "Hamburguesas", 2800, 16),
            ("Hamburguesa Texana", "Hamburguesas", 3900, 9),
            ("Hamburguesa Mexicana", "Hamburguesas", 3700, 10),
            ("Hamburguesa Blue Cheese", "Hamburguesas", 4000, 7),
            ("Hamburguesa Kids", "Hamburguesas", 1800, 20),

            # Pizzas (12)
            ("Pizza Margherita", "Pizzas", 3200, 8),
            ("Pizza Napolitana", "Pizzas", 3800, 6),
            ("Pizza Fugazzeta", "Pizzas", 4200, 5),
            ("Pizza Muzzarella", "Pizzas", 2800, 12),
            ("Pizza Calabresa", "Pizzas", 3600, 7),
            ("Pizza Jamon y Morron", "Pizzas", 3400, 9),
            ("Pizza Cuatro Quesos", "Pizzas", 4500, 5),
            ("Pizza Rucula y Jamon Crudo", "Pizzas", 4800, 4),
            ("Pizza Especial de la Casa", "Pizzas", 5000, 6),
            ("Pizza Vegetariana", "Pizzas", 3500, 8),
            ("Pizza Pepperoni", "Pizzas", 3700, 10),
            ("Pizza Provolone", "Pizzas", 3900, 6),

            # Empanadas (10)
            ("Empanadas de Carne", "Empanadas", 180, 50),
            ("Empanadas de Pollo", "Empanadas", 180, 40),
            ("Empanadas de Jamon y Queso", "Empanadas", 180, 30),
            ("Empanadas de Humita", "Empanadas", 200, 25),
            ("Empanadas de Verdura", "Empanadas", 180, 35),
            ("Empanadas de Carne Picante", "Empanadas", 200, 20),
            ("Empanadas de Roquefort", "Empanadas", 220, 15),
            ("Empanadas Arabes", "Empanadas", 200, 25),
            ("Empanadas Caprese", "Empanadas", 210, 18),
            ("Empanadas de Atun", "Empanadas", 220, 20),

            # Parrilla (10)
            ("Choripan", "Parrilla", 1200, 25),
            ("Bife de Chorizo", "Parrilla", 4500, 8),
            ("Costillas BBQ", "Parrilla", 3800, 10),
            ("Asado de Tira", "Parrilla", 4200, 7),
            ("Vacio", "Parrilla", 4800, 6),
            ("Entraña", "Parrilla", 5200, 5),
            ("Bondiola a la Parrilla", "Parrilla", 3500, 9),
            ("Pollo a la Parrilla", "Parrilla", 2800, 12),
            ("Provoleta", "Parrilla", 1500, 20),
            ("Chorizo Criollo", "Parrilla", 800, 30),

            # Pastas (10)
            ("Ravioles de Ricota", "Pastas", 3200, 10),
            ("Noquis con Salsa", "Pastas", 2800, 15),
            ("Tallarines con Tuco", "Pastas", 2500, 18),
            ("Lasagna Bolognesa", "Pastas", 3800, 8),
            ("Canelones de Verdura", "Pastas", 3400, 10),
            ("Sorrentinos de Jamon y Queso", "Pastas", 3600, 9),
            ("Fetuccini Alfredo", "Pastas", 3200, 11),
            ("Spaghetti Carbonara", "Pastas", 3500, 10),
            ("Penne al Pesto", "Pastas", 3000, 12),
            ("Lasagna de Verduras", "Pastas", 3600, 7),

            # Ensaladas (8)
            ("Ensalada Cesar", "Ensaladas", 1800, 18),
            ("Ensalada Mixta", "Ensaladas", 1500, 20),
            ("Ensalada Caprese", "Ensaladas", 2000, 15),
            ("Ensalada Griega", "Ensaladas", 2200, 12),
            ("Ensalada de Pollo", "Ensaladas", 2500, 10),
            ("Ensalada Waldorf", "Ensaladas", 2300, 8),
            ("Ensalada de Quinoa", "Ensaladas", 2400, 9),
            ("Ensalada de Rucula y Parmesano", "Ensaladas", 2100, 14),

            # Bebidas (12)
            ("Coca Cola 500ml", "Bebidas", 300, 60),
            ("Agua Mineral 500ml", "Bebidas", 200, 80),
            ("Cerveza Quilmes", "Bebidas", 400, 45),
            ("Jugo Natural de Naranja", "Bebidas", 350, 30),
            ("Sprite 500ml", "Bebidas", 300, 50),
            ("Fanta 500ml", "Bebidas", 300, 50),
            ("Cerveza Corona", "Bebidas", 600, 30),
            ("Cerveza Heineken", "Bebidas", 650, 25),
            ("Agua Saborizada", "Bebidas", 250, 40),
            ("Limonada", "Bebidas", 400, 25),
            ("Cafe Americano", "Bebidas", 350, 100),
            ("Cafe con Leche", "Bebidas", 400, 100),

            # Postres (10)
            ("Flan Casero", "Postres", 800, 15),
            ("Helado 1/4kg", "Postres", 1200, 20),
            ("Tiramisu", "Postres", 950, 12),
            ("Brownie con Helado", "Postres", 1100, 14),
            ("Cheesecake", "Postres", 1000, 10),
            ("Panqueques con Dulce de Leche", "Postres", 900, 16),
            ("Mousse de Chocolate", "Postres", 850, 12),
            ("Ensalada de Frutas", "Postres", 700, 18),
            ("Torta de Chocolate", "Postres", 950, 10),
            ("Crema Catalana", "Postres", 880, 8),
        ]

        productos_creados = 0
        for nombre, categoria_nombre, precio, stock in productos_data:
            producto, created = Producto.objects.get_or_create(
                nombre=nombre,
                categoria=categorias[categoria_nombre],
                defaults={
                    'precio': precio,
                    'stock': stock
                }
            )
            if created:
                productos_creados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\nMenu cargado exitosamente!'
            )
        )
        self.stdout.write(
            f'  {len(categorias)} categorias'
        )
        self.stdout.write(
            f'  {productos_creados} productos nuevos'
        )
