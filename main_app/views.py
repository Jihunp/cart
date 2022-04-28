from django.shortcuts import render
from .models import ShippingAddress, User, Customer, Product, Order, OrderItem, ShippingAddress


def store(request):
    context ={}
    return render(request, 'store.html', context)

def cart(request):
    context ={}
    return render(request, 'cart.html', context)

def checkout(request):
    context ={}
    return render(request, 'checkout.html', context)