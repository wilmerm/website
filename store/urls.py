
from django.urls import path

from . import views



urlpatterns = [
    path("", views.ItemListView.as_view(), name="store"),
    path("articulos/", views.ItemListView.as_view(), name="store-item-list"),
    path("articulos/<slug:slug>/", views.ItemDetailView.as_view(), name="store-item-detail"),
    path("carrito/", views.CartView.as_view(), name="store-cart"),
    path("carrito/add/", views.cart_add, name="store-cart-add"),



]
