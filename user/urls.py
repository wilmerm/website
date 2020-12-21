
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views






urlpatterns = [
    
    path("profile/", views.profile_view, name="user-profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="user-profile-update"),
    
    path("json/google-signin", views.google_signin_view, name="user-google-signin"),
    
    # auth urls.
    # Tienen que estar primero que el include 'django.contrib.auth.urls.
    # Algunas templates fueron puestas con un '2' al final del nombre para que 
    # pudieran funcionar.
    path('logout/', auth_views.LogoutView.as_view(template_name="registration/logout.html"), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form2.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done2.html"), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form2.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done2.html"), name="password_reset_done"),
    path('', include('django.contrib.auth.urls')),


]