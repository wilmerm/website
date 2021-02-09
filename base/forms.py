from django import forms

from base.models import Message



class MessageForm(forms.ModelForm):
    """Formulario para el modelo Message."""

    class Meta:
        model = Message
        fields = "__all__"

    