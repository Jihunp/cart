from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('product', views.ProductList.as_view(), name="product_list"),
    path('product/new/', views.ProductCreate.as_view(), name="product_create"),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name="product_detail"),
    path('product/<int:pk>/update', views.ProductUpdate.as_view(), name="product_update"),
    path('product/<int:pk>/delete', views.ProductDelete.as_view(), name="product_delete"),
]