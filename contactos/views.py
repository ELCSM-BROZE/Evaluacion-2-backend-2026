from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactoForm
from .models import Contacto


def lista_contactos(request):
    consulta = request.GET.get("q", "").strip()
    contactos = Contacto.objects.all()
    if consulta:
        contactos = contactos.filter(
            Q(nombre__icontains=consulta) | Q(email__icontains=consulta)
        )

    paginator = Paginator(contactos, 10)
    pagina = request.GET.get("page")
    contactos_paginados = paginator.get_page(pagina)

    return render(
        request,
        "contactos/lista_contactos.html",
        {"contactos": contactos_paginados, "consulta": consulta},
    )


def crear_contacto(request):
    form = ContactoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contacto = form.save()
        messages.success(request, f'El contacto "{contacto.nombre}" fue creado correctamente.')
        return redirect("contactos:lista_contactos")

    return render(
        request,
        "contactos/formulario_contacto.html",
        {"form": form, "titulo": "Nuevo contacto", "boton": "Guardar contacto"},
    )


def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    form = ContactoForm(request.POST or None, instance=contacto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request, f'El contacto "{contacto.nombre}" fue actualizado correctamente.'
        )
        return redirect("contactos:lista_contactos")

    return render(
        request,
        "contactos/formulario_contacto.html",
        {
            "form": form,
            "contacto": contacto,
            "titulo": "Editar contacto",
            "boton": "Guardar cambios",
        },
    )


def eliminar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == "POST":
        nombre = contacto.nombre
        contacto.delete()
        messages.success(request, f'El contacto "{nombre}" fue eliminado correctamente.')
        return redirect("contactos:lista_contactos")

    return render(
        request,
        "contactos/confirmar_eliminacion.html",
        {"contacto": contacto},
    )
