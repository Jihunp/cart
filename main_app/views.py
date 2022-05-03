from itertools import product
from django.shortcuts import render
from .models import ShippingAddress, User, Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import datetime
import json


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # get cart items is also listed inside models as a function
        userItem = order.get_cart_items
    else:
        # empty list for now but will be updated in the future
        items = []
        # unregistered user will not see anything for now
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'ship': False}
        userItem = order['get_cart_items']

    products = Product.objects.all()
    context ={'products': products, 'userItem': userItem}
    return render(request, 'store.html', context)

def cart(request):
    # query an object if it doesn't exist it creates one
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        userItem = order.get_cart_items

    else:
        # empty list for now but will be updated in the future
        items = []
        # unregistered user will not see anything for now
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'ship': False}
        userItem = order['get_cart_items']

    context ={'items':items, 'order': order, 'userItem': userItem}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        userItem = order.get_cart_items
    else:
        # empty list for now but will be updated in the future
        items = []
        # unregistered user will not see anything for now
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'ship': False }
        userItem = order['get_cart_items']

    context ={'items':items, 'order': order, "userItem": userItem}
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

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    print('data:', request.body)
    return JsonResponse('Payment complete!', safe=False)

# adding a line to test heroku deployment