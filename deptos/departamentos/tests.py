from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from .models import Departamento, Foto, Comentario
from usuarios.models import Usuario, Mensaje
from django.test import TestCase
from django.contrib.auth import logout, login, authenticate
from PIL import Image
import tempfile
from django.test import override_settings
from django.utils import timezone

from .forms import DepartamentoForm, ComentarioForm
from usuarios.forms import MensajeForm

class UrlDepartamentosTests(TestCase):

    def test_list(self):
        self.assertEqual(reverse('home'), '/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/').view_name, 'home')

class DepartamentosCrearTests(TestCase):

    def test_AltaDeptos_no_login(self):
        #Al intentar crear un nuevo depto, si no estamos logueados, nos redirige al template de login
        response = self.client.get(reverse("alquiler_crear"))
        self.assertRedirects(response, '/ingresar/?next=/nuevoAlquiler')

    def test_altaDeptos_templates_used(self):
        self.user = User.objects.create_user("test1", "test@g.com", "12345")
        Usuario(usuario=self.user).save()
        self.client.login(username='test1', password='12345')
        # testea que usamos el template 'departamentos/departamento_form.html'
        response = self.client.get(reverse('alquiler_crear'))
        self.assertTemplateUsed(response, 'departamentos/departamento_form.html')

    def test_AltaDeptos_view(self):
        self.user = User.objects.create_user("test1", "test@g.com", "12345")
        Usuario(usuario=self.user).save()
        self.client.login(username='test1', password='12345')
        # datos en context de la vista
        # por get, llega el form.
        response = self.client.get(reverse('alquiler_crear'))
        self.assertTrue("form" in response.context)
        self.assertTrue(isinstance(response.context["form"], DepartamentoForm))

    def test_crear_alquiler(self):
        # Que se crean departamentos y se visualizan correctamente en el contexto "alquileres"...
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
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
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        response = self.client.post(reverse('alquiler_crear'), {
            'titulo': 'testing',
			'descripcion': 'descrip_test',
			'latitud': 30.000,
			'longitud': 10.000,
			'capacidad': 5,
			'localidad': 'San Rafael',
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

class DepartamentosActualizarTests(TestCase):

    def test_editarAlquiler_templates_used(self):
        #Logueamos y creamos un usuario default...
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)

        #Creamos un alquiler...
        alquilertest = Departamento.objects.create(titulo='titulotest', descripcion='asdtest', latitud=11.111, longitud=22.2222, capacidad=4, localidad='localidadtest', precio=10000,usuario=usuariotest)

        # testea que usamos el template 'departamentos/departamento_form.html' al editar...
        response = self.client.get(reverse('alquiler_editar', args=(alquilertest.pk,)))
        self.assertTemplateUsed(response, 'departamentos/departamento_form_edit.html')

    def test_editarAlquiler_context_view(self):
        #Logueamos y creamos un usuario default...
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)

        #Creamos un alquiler por default...
        alquilertest = Departamento.objects.create(titulo='titulotest', descripcion='asdtest', latitud=11.111, longitud=22.2222, capacidad=4, localidad='localidadtest', precio=10000,usuario=usuariotest)

        # datos en context de la vista
        # por get, llega el form.
        response = self.client.get(reverse('alquiler_editar', args=(alquilertest.pk,)))
        self.assertTrue("form" in response.context)
        self.assertTrue(isinstance(response.context["form"], DepartamentoForm))

    def test_editarAlquiler_post(self):
        #Logueamos y creamos un usuario default...
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)

        #Creamos un alquiler por default...
        alquilertest = Departamento.objects.create(titulo='titulotest', descripcion='asdtest', latitud=11.111, longitud=22.2222, capacidad=4, localidad='Junín', precio=10000,usuario=usuariotest)

        #Actualizamos datos y obtenemos respuesta exitosa
        response = self.client.post(reverse('alquiler_editar', args=(alquilertest.pk,)), {
            'titulo': 'new titulotest',
			'descripcion': 'new asdtest',
			'latitud': 12.123,
			'longitud': 23.456,
			'capacidad': 3,
            'localidad': 'San Rafael',
            'precio': 5000,
            'usuario': usuariotest,
        })
        self.assertEqual(response.status_code, 302)
        #Comprobamos la actualizacion de los datos...
        self.assertEqual(Departamento.objects.filter(titulo="new titulotest").count(), 1)
        self.assertTrue(Departamento.objects.filter(precio=5000).exists())

class DepartamentosBorradoTests(TestCase):

    def test_borrarAlquiler_templates_used(self):
        #Logueamos y creamos un usuario default...
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)

        #Creamos un alquiler por default...
        alquilertest = Departamento.objects.create(titulo='titulotest', descripcion='asdtest', latitud=11.111, longitud=22.2222, capacidad=4, localidad='localidadtest', precio=10000,usuario=usuariotest)

        # testea que usamos el template 'departamentos/departamento_form.html' al editar...
        response = self.client.get(reverse('alquiler_borrar', args=(alquilertest.pk,)))
        self.assertTemplateUsed(response, 'departamentos/borrado_alquiler.html')

    def test_borrarAlquiler(self):
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        # Creo depto nº1..
        Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=10.000, longitud=10.000,capacidad=1,precio=1000,usuario=usuariotest)
        # Creo depto nº2..
        Departamento.objects.create(titulo="titulo2", descripcion="descrip2", latitud=20.000, longitud=20.000,capacidad=2,precio=2000,usuario=usuariotest)
        resp = self.client.get(reverse('home'))
        # Debe identificar 2 alquileres creados en el listado...
        self.assertEqual(len(resp.context["alquileres"]), 2)
        # Borramos uno y deberá actualizarse a 1 la cantidad de alquileres...
        depto = Departamento.objects.get(pk=1)
        depto.delete();
        resp = self.client.get(reverse('home'))
        self.assertEqual(len(resp.context["alquileres"]), 1)
        self.assertTrue(Departamento.objects.filter(titulo='titulo2').exists())

class DepartamentoDisableEnableTest(TestCase):

    def test_DisableEnableAlquiler(self):
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        # Creo depto nº1...
        alquilertest=Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=10.000, longitud=10.000,capacidad=1,precio=1000,usuario=usuariotest)
        #Luego de get a deshabilitar con respuesta exitosa...
        depto = Departamento.objects.get(pk=1)
        response = self.client.get(reverse('alquiler_desactivar', args=(depto.pk,)))
        self.assertEqual(response.status_code, 302)
        #Activo el alquiler...
        response = self.client.get(reverse('alquiler_activar', args=(depto.pk,)))
        self.assertEqual(response.status_code, 302)

class DetalleDepartamentosTests(TestCase):

    def test_details(self):
        self.assertEqual(reverse('details', args=[1]), '/details/1/')

    def test_details_resolve(self):
        self.assertEqual(resolve('/details/1/').view_name, 'details')

    def test_details_datos(self):
        #Logueo con un usuario...
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        #Creo depto
        depto = Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=10.000, longitud=10.000,capacidad=1,precio=1000,usuario=usuariotest)
        #Creo imagen
        temp_file = tempfile.NamedTemporaryFile()
        size = (200, 200)
        color = (255, 0, 0, 0)
        image = Image.new("RGBA", size, color)
        image.save(temp_file, 'jpeg')
        test_image = temp_file
        #Creo foto
        foto = Foto.objects.create(departamento=depto, imagen=test_image.name)
        comment = Comentario.objects.create(texto="Buen depto", emisor=usuariotest, fecha_envio=timezone.now(), departamento=depto)
        self.assertEqual(len(Foto.objects.all()), 1)
        self.assertEqual(len(Comentario.objects.all()), 1)
        self.assertEqual(depto.foto_set.all()[0].imagen, test_image.name)
        self.assertEqual(depto.comentario_set.all()[0].texto, "Buen depto")
        self.assertEqual(depto.comentario_set.all()[0].texto, comment.texto)
        self.assertEqual(foto.departamento.titulo, "titulo1")
        self.assertEqual(len(Foto.objects.all()), len(depto.foto_set.all()))
        self.assertEqual(len(Comentario.objects.all()), len(depto.comentario_set.all()))

        response = self.client.get(reverse('details', args=[1]))
        self.assertTrue("form1" in response.context)
        self.assertTrue(isinstance(response.context["form1"], ComentarioForm))
        self.assertTrue("form2" in response.context)
        self.assertTrue(isinstance(response.context["form2"], MensajeForm))

    def test_details_comentario(self):
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        depto = Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=10.000, longitud=10.000, capacidad=1, precio=1000, usuario=usuariotest)
        response = self.client.post(reverse('details_comentario', args=[1]), {
            'texto': 'Comentario de prueba',
			'emisor': usuariotest,
			'fecha_envio': timezone.now(),
            'departamento': depto,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/details/1/")
        self.assertEqual(Comentario.objects.filter(texto="Comentario de prueba").count(), 1)

    def test_details_mensaje(self):
        user1 = User.objects.create(username='testuser1')
        user1.set_password('12345')
        user1.save()
        user2 = User.objects.create(username='testuser2')
        user2.set_password('12345')
        user2.save()
        self.client.login(username='testuser1', password='12345')
        usuariotest1 = Usuario.objects.create(telefono="333333", direccion="dir_test1", usuario=user1)
        usuariotest2 = Usuario.objects.create(telefono="333332", direccion="dir_test2", usuario=user2)
        Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=10.000, longitud=10.000, capacidad=1, precio=1000, usuario=usuariotest1)
        response = self.client.post(reverse('details_mensaje', args=[1]), {
            'texto': 'Mensaje de prueba',
			'emisor': usuariotest1,
            'receptor': usuariotest2,
			'fecha_envio': timezone.now(),
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/details/1/")
        self.assertEqual(Mensaje.objects.filter(texto="Mensaje de prueba").count(), 1)

class Buscadordeptotest(TestCase):

    def test_search(self):
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
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

class FiltroCapacidad(TestCase):

    def test_capacidad(self):
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        # Creo depto n°1..
        Departamento.objects.create(titulo="titulo1", descripcion="descrip1", latitud=13.000, longitud=7.000,capacidad=1,precio=15000,usuario=usuariotest)
        # Creo depto n°2..
        Departamento.objects.create(titulo="titulo2", descripcion="descrip2", latitud=21.000, longitud=9.000,capacidad=2,precio=20000,usuario=usuariotest)
        # Creo depto n°3..
        Departamento.objects.create(titulo="titulo3", descripcion="mauricio", latitud=12.000, longitud=8.000,capacidad=1,precio=10000,usuario=usuariotest)

        response = self.client.get("%s?c=2" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),1)
        self.assertEqual(response.context["alquileres"].first().capacidad,2)
        response = self.client.get("%s?c=" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),Departamento.objects.count())
        response = self.client.get("%s?c=5" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),0)

class FiltroLocalidad(TestCase):

    def test_localidad(self):
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        # Creo depto n°1..
        Departamento.objects.create(titulo="titulo1", descripcion="descrip1",localidad="San Rafael",latitud=13.000, longitud=7.000,capacidad=1,precio=15000,usuario=usuariotest)
        # Creo depto n°2..
        Departamento.objects.create(titulo="titulo2", descripcion="descrip2",localidad="Gnral. Alvear", latitud=21.000, longitud=9.000,capacidad=2,precio=20000,usuario=usuariotest)
        # Creo depto n°3..
        Departamento.objects.create(titulo="titulo3", descripcion="mauricio",localidad="San Rafael", latitud=12.000, longitud=8.000,capacidad=1,precio=10000,usuario=usuariotest)

        response = self.client.get("%s?l=S" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),2)
        self.assertEqual(response.context["alquileres"].first().localidad,"San Rafael")
        response = self.client.get("%s?l=" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),Departamento.objects.count())
        response = self.client.get("%s?l=M" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),0)

class FiltroPrecio(TestCase):

    def test_precio(self):
        user = User.objects.create_user("test1", "test@g.com", "12345")
        user.save()
        self.client.login(username='test1', password='12345')
        usuariotest = Usuario.objects.create(telefono="333333", direccion="dir_test", usuario=user)
        # Creo depto n°1..
        Departamento.objects.create(titulo="titulo1", descripcion="descrip1", localidad="San Rafael", latitud=13.000, longitud=7.000,capacidad=1,precio=10000,usuario=usuariotest)
        # Creo depto n°2..
        Departamento.objects.create(titulo="titulo2", descripcion="descrip2", localidad="San Rafael", latitud=21.000, longitud=9.000,capacidad=2,precio=20000,usuario=usuariotest)
        # Creo depto n°3..
        Departamento.objects.create(titulo="titulo3", descripcion="mauricio", localidad="San Rafael", latitud=12.000, longitud=8.000,capacidad=1,precio=15000,usuario=usuariotest)

        response = self.client.get("%s?p=15000" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),2)
        self.assertEqual(response.context["alquileres"].first().precio,10000)
        response = self.client.get("%s?p=" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(),Departamento.objects.count())
        response = self.client.get("%s?p=25000" % reverse("home"))
        self.assertEqual(response.context["alquileres"].count(), 3)
