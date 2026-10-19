from django.db import models

# Create your models here.
class Contacto(models.models):
    nombre = models.CharField(max_length=100)
    Email = models.TextField(blank=True)
    Localidad = models.PositiveIntegerField()
    Numero = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre