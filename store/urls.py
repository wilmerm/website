
from django.urls import path

from . import views



urlpatterns = [
    path("articulos/", views.ItemListView.as_view(), name="store-item-list"),


]
