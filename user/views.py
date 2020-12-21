
import random

from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import (CreateView, UpdateView, ListView)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .authentication import google_verify_token
from .models import User




def profile_view(request):
    """
    Se muestra el perfil del actual usuario logueado.
    """
    return render(request, "user/profile.html", context={})




class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    El usuario actual modifica sus propios datos.
    """
    model = User
    fields = ("first_name", "last_name", "phone1", "phone2", "address")
    template_name = "user/profile_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self):
        """
        Enviaremos siempre el usuario actual logueado.
        """
        return self.request.user




def google_signin_view(request):
    """
    Inicio de sesión o registro de usuarios usando la API de Google.
    
    """
    try:
        google_user = google_verify_token(request)
    except (ValueError) as e:
        if request.user.is_superuser:
            return JsonResponse({"error": True, "message": str(e)})
        return JsonResponse({})

    print("google_signin_view(request): ", google_user)

    # En este punto el usuario se ha validado correctamente.
    idinfo = google_user["idinfo"]
    user = None

    # Si hay un usuario autenticado.
    if request.user.is_authenticated:
        # Si el usuario que intenta loguearse es el mismo que ya está logueado,
        # actualizamos algunos de sus datos.
        if request.user.email == idinfo["email"]:
            user = request.user
            if google_user["idinfo"]["picture"]:
                user.image_url = idinfo["picture"]
                user.google_userid = idinfo["sub"]
            user.save()
        else:
            # Continuamos en la siguiente condición.
            user = None

    # Si el usuario no es el mismo que ya está logueado o no hay nadie logueado,
    # procedemos a loguear el usuario de Google o registrarlo si no lo tenemos
    # registrado.
    if not user:
        try:
            user = User.on_site.get(email=idinfo["email"])
        except (User.DoesNotExist):
            # Registramos el usuario.

            # Generamos una contraseña aleatoria.
            sr = "a b c d e f g h i j k l m n o p k r s t u v w k y z A B C D "
            "E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9"
            random.shuffle(sr.split())
            pwd = sr[:10]

            user = User.objects.create_user(username=idinfo["email"], password=pwd)
            user.initial_password = pwd
            user.email = idinfo["email"]
            user.first_name = idinfo["given_name"]
            user.last_name = idinfo["family_name"]
            user.image_url = idinfo["picture"]
            user.google_userid = idinfo["sub"]
            user.is_active = True
            user.clean()
            user.save()

            google_user["initial_password"] = pwd
            messages.success(request, _("¡Su cuenta ha sido creada correctamente!"))
            messages.info(request, _("Se ha generado una contraseña "
            f"aleatoria que podrá cambiar en cualquier momento. Contraseña: {pwd}"))
        else:
            messages.info(request, _("¡Usted ha ingresado con su cuenta de "
            "Google correctamente!"))
        # Logueamos el usuario.
        # 'user.authentication.AuthByEmailBackend',
        # 'django.contrib.auth.backends.ModelBackend',
        login(request, user, backend="user.authentication.AuthByEmailBackend")

    return JsonResponse(google_user)