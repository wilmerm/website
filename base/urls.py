
from django.urls import path

from . import views



urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("acerca-de/", views.AboutView.as_view(), name="about"),
    path("marcas/", views.BrandsView.as_view(), name="brands"),
    path("calculadora-btu/", views.CalcBTUView.as_view(), name="calcbtu"),
    path("preguntas-frecuentes/", views.QuestionsView.as_view(), name="questions"),
    path("policy/", views.PolicyView.as_view(), name="policy"),
    path("contact/", views.contact_view, name="contact"),

]
