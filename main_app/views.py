from django.shortcuts import render
from .models import ShippingAddress, User, Customer, Product, Order, OrderItem, ShippingAddress


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
    context ={'items':items, 'order': order}
    return render(request, 'cart.html', context)

def checkout(request):
    context ={}
    return render(request, 'checkout.html', context)