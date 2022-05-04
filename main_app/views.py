from ctypes import addressof
from itertools import product
from django.shortcuts import render
from .models import ShippingAddress, User, Customer, Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import datetime
import json
# for crud functionality
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

# crud for products
# icebox feature so in the future only admin user can have access to create and update items
class ProductList(TemplateView):
    template_name = 'store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["product"] = Product.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"
        else:
            context["product"] = Product.objects.all()
            context["header"] = "product"
        return context

class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    # fields = ['name', 'price', 'description', 'tangible', 'image']
    template_name = 'product_create.html'
    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/product')

class ProductDetail(DetailView):
    model = Product
    template_name = "product_detail.html"


class ProductUpdate(UpdateView):
    model = Product
    # fields = ['name', 'price', 'description', 'tangible', 'image']
    fields = '__all__'
    template_name = "product_update.html"
    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})

class ProductDelete(DeleteView):
    model = Product
    template_name = "product_delete_confirm.html"
    success_url = "/product"


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
    transaction_id = datetime.datetime.now().timestamp()
    # parse and access json data
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.ship == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['ship']['address'],
                city=data['ship']['city'],
                state=data['ship']['state'],
                zipcode=data['ship']['zipcode'],

            )


    else:
        print('User needs to be logged in')
    return JsonResponse('Payment complete!', safe=False)

# adding a line to test heroku deployment