import csv
import io

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .admin import ContactoAdmin, exportar_contactos_csv
from .models import Contacto


class ContactosViewsTests(TestCase):
    def setUp(self):
        self.contacto = Contacto.objects.create(
            nombre="Ana Pérez",
            email="ana@example.com",
            telefono="+56 9 1234 5678",
            localidad="Santiago",
            direccion="Calle 1",
            notas="Amiga",
        )

    def test_lista_contactos_y_busqueda(self):
        response = self.client.get(reverse("contactos:lista_contactos"), {"q": "ana"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ana Pérez")

    def test_busca_por_correo(self):
        response = self.client.get(
            reverse("contactos:lista_contactos"), {"q": "example.com"}
        )

        self.assertContains(response, "Ana Pérez")

    def test_crea_contacto(self):
        response = self.client.post(
            reverse("contactos:crear_contacto"),
            {
                "nombre": "Luis Soto",
                "email": "luis@example.com",
                "telefono": "012345678",
                "localidad": "Valparaíso",
                "direccion": "",
                "notas": "",
                "activo": "on",
            },
        )

        self.assertRedirects(response, reverse("contactos:lista_contactos"))
        self.assertTrue(Contacto.objects.filter(nombre="Luis Soto").exists())

    def test_rechaza_correo_invalido(self):
        response = self.client.post(
            reverse("contactos:crear_contacto"),
            {"nombre": "Luis Soto", "email": "correo-invalido"},
        )

        self.assertEqual(response.status_code, 200)
        error = response.context["form"].errors.as_data()["email"][0]
        self.assertEqual(error.code, "invalid")

    def test_edita_contacto(self):
        response = self.client.post(
            reverse("contactos:editar_contacto", args=[self.contacto.pk]),
            {
                "nombre": "Ana Pérez",
                "email": "ana.nueva@example.com",
                "telefono": self.contacto.telefono,
                "localidad": self.contacto.localidad,
                "direccion": self.contacto.direccion,
                "notas": self.contacto.notas,
                "activo": "on",
            },
        )

        self.assertRedirects(response, reverse("contactos:lista_contactos"))
        self.contacto.refresh_from_db()
        self.assertEqual(self.contacto.email, "ana.nueva@example.com")

    def test_elimina_contacto_solo_por_post(self):
        url = reverse("contactos:eliminar_contacto", args=[self.contacto.pk])
        self.assertEqual(self.client.get(url).status_code, 200)

        response = self.client.post(url)

        self.assertRedirects(response, reverse("contactos:lista_contactos"))
        self.assertFalse(Contacto.objects.filter(pk=self.contacto.pk).exists())


class ContactosAdminTests(TestCase):
    def test_admin_busca_por_nombre_y_email(self):
        ana = Contacto.objects.create(nombre="Ana Pérez", email="ana@example.com")
        juan = Contacto.objects.create(nombre="Juan Soto", email="juan@example.com")
        admin_contactos = ContactoAdmin(Contacto, AdminSite())
        request = RequestFactory().get("/admin/contactos/contacto/")

        por_nombre, _ = admin_contactos.get_search_results(
            request, Contacto.objects.all(), "Ana"
        )
        por_email, _ = admin_contactos.get_search_results(
            request, Contacto.objects.all(), "juan@example.com"
        )

        self.assertEqual(set(por_nombre.values_list("pk", flat=True)), {ana.pk})
        self.assertEqual(set(por_email.values_list("pk", flat=True)), {juan.pk})

    def test_exporta_contactos_seleccionados_a_csv(self):
        contacto = Contacto.objects.create(
            nombre='=HYPERLINK("https://example.com")',
            email="ana@example.com",
            notas="Nota",
        )
        request = RequestFactory().get("/admin/contactos/contacto/")
        admin_contactos = ContactoAdmin(Contacto, AdminSite())
        response = exportar_contactos_csv(
            admin_contactos, request, Contacto.objects.filter(pk=contacto.pk)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="contactos.csv"',
        )
        rows = list(csv.reader(io.StringIO(response.content.decode("utf-8-sig"))))
        self.assertEqual(rows[0][0], "Nombre")
        self.assertEqual(rows[1][0], '\t=HYPERLINK("https://example.com")')
