from django.urls import path

from . import views

app_name = "contactos"

urlpatterns = [
    path("", views.lista_contactos, name="lista_contactos"),
    path("nuevo/", views.crear_contacto, name="crear_contacto"),
    path("<int:pk>/editar/", views.editar_contacto, name="editar_contacto"),
    path("<int:pk>/eliminar/", views.eliminar_contacto, name="eliminar_contacto"),
]
