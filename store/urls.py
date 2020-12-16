
from django.urls import path

from . import views



urlpatterns = [
    path("", views.ItemListView.as_view(), name="store"),
    path("articulos/", views.ItemListView.as_view(), name="store-item-list"),
    path("articulos/<slug:slug>/", views.ItemDetailView.as_view(), name="store-item-detail"),
    path("carrito/", views.CartView.as_view(), name="store-cart"),
    path("orden/create/", views.OrderCreateView.as_view(), name="store-order-create"),
    path("orden/list/<int:pk>/", views.OrderDetailView.as_view(), name="store-order-detail"),
    path("json/cart/get/", views.cart_get, name="store-cart-get"),
    path("json/cart/add/", views.cart_add, name="store-cart-add"),
    path("json/cart/remove/", views.cart_remove, name="store-cart-remove"),
    path("json/cart/update/", views.cart_update, name="store-cart-update"),
    #path("checkout/", views.checkout, name="store-checkout")



]
