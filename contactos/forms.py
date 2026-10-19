from django import forms

from .models import Contacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = (
            "nombre",
            "email",
            "telefono",
            "localidad",
            "direccion",
            "notas",
            "activo",
        )
