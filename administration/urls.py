from django.urls import path 

from administration import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="administration-index"),
    path("message/<int:pk>/", views.MessageUpdateView.as_view(),
    name="administration-message"),
]