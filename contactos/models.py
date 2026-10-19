from django.db import models


class Contacto(models.Model):
    nombre = models.CharField("nombre", max_length=100)
    email = models.EmailField("correo electrónico", blank=True)
    telefono = models.CharField("teléfono", max_length=30, blank=True)
    localidad = models.CharField("localidad", max_length=100, blank=True)
    direccion = models.CharField("dirección", max_length=200, blank=True)
    notas = models.TextField("notas", blank=True)
    activo = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ("nombre", "pk")
        verbose_name = "contacto"
        verbose_name_plural = "contactos"

    def __str__(self):
        return self.nombre
