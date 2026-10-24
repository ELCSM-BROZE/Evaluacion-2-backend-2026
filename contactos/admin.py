import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Contacto


def _valor_csv_seguro(valor):
    texto = str(valor)
    if texto.lstrip().startswith(("=", "+", "-", "@")):
        return f"\t{texto}"
    return texto


@admin.action(description="Exportar contactos seleccionados a CSV")
def exportar_contactos_csv(_modeladmin, _request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="contactos.csv"'
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow(
        (
            "Nombre",
            "Correo electrónico",
            "Teléfono",
            "Localidad",
            "Dirección",
            "Notas",
            "Activo",
        )
    )
    for contacto in queryset.iterator():
        writer.writerow(
            _valor_csv_seguro(valor)
            for valor in (
                contacto.nombre,
                contacto.email,
                contacto.telefono,
                contacto.localidad,
                contacto.direccion,
                contacto.notas,
                "Sí" if contacto.activo else "No",
            )
        )
    return response


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono", "localidad", "activo")
    list_filter = ("activo", "localidad")
    search_fields = ("nombre", "email")
    ordering = ("nombre", "pk")
    list_per_page = 10
    actions = (exportar_contactos_csv,)

    def changelist_view(self, request, extra_context=None):
        self.admin_site.site_header = "Agenda personal"
        self.admin_site.site_title = "Agenda personal"
        self.admin_site.index_title = "Administración de contactos"
        return super().changelist_view(request, extra_context=extra_context)
