from django.db import models
from django.contrib.auth.models import User
# Create your models here.
''' Decorador @propery, este decorador nos permite
   convertir un metodo en en una propiedad, "objeto.metodo",
   en vez de "objeto.metodo()", convirtiendose a propiedad podriamos
   cambiar su valor al asignarlo, "objeto.metodo=5", esto se aria con un
   decorador "setter".
'''


class Cliente(models.Model):
    # Crea la relacion con el modelo usuario
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=70, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Producto(models.Model):
    name = models.CharField(max_length=70, null=True)
    precio = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    # Nos ayudara a subir las imagenes de forma dinamica
    imagen = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # exepcion que ocurrira al no encontrar la imagen
    @property
    def imagen_url(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url


# Es el pedido que se mostrara en el carrito
class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_pedido = models.DateField(auto_now_add=True)
    completado = models.BooleanField(default=False, null=True, blank=False)
    transaccion_id = models.CharField(max_length=70, null=True)

    def __str__(self):
        return str(self.transaccion_id)

    # precio total de los productos
    @property
    def get_carrito_total(self):
        pedidoitems = self.pedidoitem_set.all()
        total = sum([item.get_total for item in pedidoitems])
        return total

    # Todos los productos
    @property
    def get_carrito_items(self):
        pedidoitems = self.pedidoitem_set.all()
        total = sum([item.cantidad for item in pedidoitems])
        return total

# Un pedido podra tener multiple pedido_item


class PedidoItem(models.Model):
    # Que producto tiene
    producto = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, blank=True, null=True)
    # A que pedido pertenece
    Pedido = models.ForeignKey(
        Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField(default=0, null=True)
    fecha = models.DateField(auto_now_add=True)

    # este metodo calcula el total de los productos
    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total


class Direccion_envio(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(
        Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    direccion = models.CharField(max_length=70, null=True)
    ciudad = models.CharField(max_length=70, null=True)
    estado = models.CharField(max_length=70, null=True)
    codigo_postal = models.CharField(max_length=70, null=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.direccion
