from itertools import product
from django.shortcuts import render
from .models import ShippingAddress, User, Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import json


def store(request):
    products = Product.objects.all()
    context ={'products': products}
    return render(request, 'store.html', context)

def cart(request):
    # query an object if it doesn't exist it creates one
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # empty list for now but will be updated in the future
        items = []
        # unregistered user will not see anything for now
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context ={'items':items, 'order': order}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # empty list for now but will be updated in the future
        items = []
        # unregistered user will not see anything for now
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context ={'items':items, 'order': order}
    return render(request, 'checkout.html', context)

def updateItem(request):
    # post request
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # conditional statement that adds quantity of items in user's order or removes one.
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quanity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)