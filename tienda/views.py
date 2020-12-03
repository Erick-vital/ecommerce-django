from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json

# Create your views here.


def tienda(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        # Crea o encontra el pedido
        pedido, creado = Pedido.objects.get_or_create(
            cliente=cliente, completado=False)
        items = pedido.pedidoitem_set.all()
        carritoItems = pedido.get_carrito_items
    else:
        items = []
        pedido = {'get_carrito_total': 0, 'get_carrito_items': 0}
        carritoItems = pedido['get_carrito_items']

    productos = Producto.objects.all()
    contexto = {'productos': productos, 'carritoItems': carritoItems}
    return render(request, 'tienda.html', contexto)


def carrito(request):

    # tienes que entrar al admin con la cuenta que relacionaste
    if request.user.is_authenticated:
        cliente = request.user.cliente
        # Crea o encontra el pedido
        pedido, creado = Pedido.objects.get_or_create(
            cliente=cliente, completado=False)
        items = pedido.pedidoitem_set.all()
        carritoItems = pedido.get_carrito_items
    else:
        items = []
        pedido = {'get_carrito_total': 0, 'get_carrito_items': 0}
        carritoItems = Pedido['get_carrito_items']

    contexto = {'items': items, 'pedido': pedido, 'carritoItems': carritoItems}
    return render(request, 'carrito.html', contexto)


def checkout(request):

    # tienes que entrar al admin con la cuenta que relacionaste
    if request.user.is_authenticated:
        cliente = request.user.cliente
        # Crea o encontra el pedido
        pedido, crear = Pedido.objects.get_or_create(
            cliente=cliente, completado=False)
        items = pedido.pedidoitem_set.all()
        carritoItems = pedido.get_carrito_items
    else:
        items = []
        pedido = {'get_carrito_total': 0, 'get_carrito_items': 0}
        carritoItems = pedido['get_carrito_items']

    contexto = {'items': items, 'pedido': pedido, 'carritoItems': carritoItems}
    return render(request, 'checkout.html', contexto)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    accion = data['accion']

    print('Producto Id: ', productId)
    print('Accion: ', accion)

    cliente = request.user.cliente
    producto = Producto.objects.get(id=productId)
    pedido, crear = Pedido.objects.get_or_create(
        cliente=cliente, completado=False)
    pedidoItem, crear = PedidoItem.objects.get_or_create(
        Pedido=pedido, producto=producto)

    if accion == 'add':
        pedidoItem.cantidad += 1
    elif accion == 'remove':
        pedidoItem.cantidad -= 1

    pedidoItem.save()

    if pedidoItem.cantidad <= 0:
        pedidoItem.delete()

    data = {'my_data': 'Item fue agregado'}
    return JsonResponse(data)
