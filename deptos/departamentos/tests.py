from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from .models import Departamento
from usuarios.models import Usuario
from django.test import TestCase
from django.contrib.auth import logout, login, authenticate

from .forms import DepartamentoForm

class UrlDepartamentosTests(TestCase):

    def test_list(self):
        self.assertEqual(reverse('home'), '/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/').view_name, 'home')

class DepartamentosCrearTests(TestCase):

    def test_altaDeptos_templates_used(self):
        # testea que usamos el template 'departamentos/departamento_form.html'
        response = self.client.get(reverse('alquiler_crear'))
        self.assertTemplateUsed(response, 'departamentos/departamento_form.html')

    def test_AltaDeptos_view(self):
        # datos en context de la vista
        # por get, llega el form.
        response = self.client.get(reverse('alquiler_crear'))
        self.assertTrue("form" in response.context)
        self.assertTrue(isinstance(response.context["form"], DepartamentoForm))

    def test_crear_alquiler(self):
        # Que se crean departamentos y se visualizan correctamente en el contexto "alquileres"...
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        # Creo depto nº1..
        Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=10.000, longitud=10.000,capacidad=1,precio=1000,usuario=usuariotest)
        # Creo depto nº2..
        Departamento.objects.create(titulo="titulo2", descripcion="descrip2", latitud=20.000, longitud=20.000,capacidad=2,precio=2000,usuario=usuariotest)
        resp = self.client.get(reverse('home'))
        # Debe identificar 2 alquileres creados en el listado...
        self.assertEqual(len(resp.context["alquileres"]), 2)


    def test_altaDeptos_post(self):
        # Que llegan los datos bien por POST
        # que se crea un alquiler nuevo en la db
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        response = self.client.post(reverse('alquiler_crear'), {
            'titulo': 'testing',
			'descripcion': 'descrip_test',
			'latitud': 30.000,
			'longitud': 10.000,
			'capacidad': 5,
			'localidad': 'loc_test',
            'precio': 6000,
            'usuario': usuariotest,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.assertEqual(Departamento.objects.filter(titulo="testing").count(), 1)
        self.assertTrue(Departamento.objects.filter(precio=6000).exists())

        # Que se crea otro alquiler y llegan datos mediante POST
        # Con error de validacion al faltar campo obligatorio "localidad"...
        response = self.client.post(reverse('alquiler_crear'), {
            'titulo': 'testing',
			'descripcion': 'descrip_test',
			'latitud': 30.000,
			'longitud': 10.000,
			'capacidad': 5,
            'precio': 6000,
            'usuario': usuariotest,
        })
        self.assertTrue("localidad" in response.context["form"].errors)

class Buscadordeptotest(TestCase):

    def test_search(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        # Creo depto n°1..
        Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=13.000, longitud=7.000,capacidad=1,precio=15000,usuario=usuariotest)
        # Creo depto n°2..
        Departamento.objects.create(titulo="titulo2", descripcion="descrip2", latitud=21.000, longitud=9.000,capacidad=2,precio=20000,usuario=usuariotest)
        # Creo depto n°3..
        Departamento.objects.create(titulo="titulo3", descripcion="mauricio", latitud=12.000, longitud=8.000,capacidad=1,precio=10000,usuario=usuariotest)

        response = self.client.get("%s?q=m" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),1)
        self.assertEqual(response.context["alquileres"].first().descripcion,"mauricio")
        response = self.client.get("%s?q=" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),Departamento.objects.count())
        response = self.client.get("%s?q=h" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),0)
