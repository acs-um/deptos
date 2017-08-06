from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.utils import timezone

from django.test import TestCase

from .forms import SignUpForm, MensajeForm
from .models import Usuario, Mensaje


class UrlUsuariosTests(TestCase):

    def test_list(self):
        self.assertEqual(reverse('signup'), '/registrar/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/registrar/').view_name, 'signup')


class SignupTests(TestCase):

    def test_signup_templates_used(self):
        # que usamos el template 'usuarios/signup.html'
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'usuarios/signup.html')

    def test_signup_view(self):
        # datos en context de la vista
        # por get, llega el form.
        response = self.client.get(reverse('signup'))
        self.assertTrue("form" in response.context)
        self.assertTrue(isinstance(response.context["form"], SignUpForm))

    def test_signup_post(self):
        # Que llegan los datos bien por POST
        # que se crea un user nuevo en la db
        response = self.client.post(reverse('signup'), {
            'username': "test1",
            'password': "123123",
            'password_confirmation': "123123",
            'email': "test@g.com",
            'first_name': "Test",
            'last_name': "Last name"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/ingresar/")

        #Se comprueba que haya sido creado en la tabla User
        self.assertEqual(User.objects.filter(username="test1").count(), 1)

        #Se comprueba que haya sido creado en la tabla Usuario
        self.assertEqual(Usuario.objects.filter(usuario__username="test1").count(), 1)

class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@g.com", "123123", first_name="First name", last_name="Last name")

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': "test",
            'password': "123123"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

class UrlReestablecimientoTests(TestCase):

    def test_urls(self):
        self.assertEqual(reverse('password_reset'), '/usuarios/reestablecer')
        self.assertEqual(reverse('password_reset_done'), '/usuarios/reestablecer/notificacion')
        self.assertEqual(reverse('password_reset_complete'), '/usuarios/reestablecer/finalizado')

    def test_resolve(self):
        self.assertEqual(resolve('/usuarios/reestablecer').view_name, 'password_reset')
        self.assertEqual(resolve('/usuarios/reestablecer/notificacion').view_name, 'password_reset_done')
        self.assertEqual(resolve('/usuarios/reestablecer/finalizado').view_name, 'password_reset_complete')

    def test_templates_used(self):
        response = self.client.get(reverse('password_reset'))
        self.assertTemplateUsed(response, 'usuarios/reestablecer/password_reset_form.html')

        response = self.client.get(reverse('password_reset_done'))
        self.assertTemplateUsed(response, 'usuarios/reestablecer/password_reset_done.html')

        response = self.client.get(reverse('password_reset_complete'))
        self.assertTemplateUsed(response, 'usuarios/reestablecer/password_reset_complete.html')

class ValidacionesRegistrarTests(TestCase):

    # Intento crear un usuario sin setear un campo obligatorio
    def test_email_obligatorio(self):
        self.client.post(reverse('signup'), {
        'username': "usertest",
        'password': "12345",
        'password_confirmation': "12345"
        })

        user = User.objects.filter(username="usertest")
        self.assertFalse(user.exists())

    # Check password y password_confirmation
    def test_password_confirmation(self):
        self.client.post(reverse('signup'), {
        'username': "usertest",
        'password': "12345",
        'password_confirmation': "12346",
        'email': "test@gmail.com"
        })

        user = User.objects.filter(username="usertest")
        self.assertFalse(user.exists())

class EditarDatosUsuarioTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("test1", "test@g.com", "12345")
        Usuario(usuario=self.user).save()

    def test_urls(self):
        self.assertEqual(reverse("perfil"), "/usuarios/perfil")
        self.assertEqual(resolve("/usuarios/perfil").view_name, 'perfil')

    def test_no_login(self):
        response = self.client.get(reverse("perfil"))
        self.assertRedirects(response, '/ingresar/?next=/usuarios/perfil')

    def test_form_edit(self):
        self.client.login(username="test1", password="12345")
        response = self.client.post(reverse('perfil'), {
            'first_name': "user",
            'last_name': "test",
            'username': "testuser",
            'email': "testuser@deptos.com",
            'direccion': "742 Evergreen Terrace",
            'telefono': "0303456",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("perfil"))

        user = Usuario.objects.get(usuario__username="testuser")
        self.assertEqual(user.usuario.first_name, "user")
        self.assertEqual(user.usuario.last_name, "test")
        self.assertEqual(user.usuario.username, "testuser")
        self.assertEqual(user.usuario.email, "testuser@deptos.com")
        self.assertEqual(user.direccion, "742 Evergreen Terrace")
        self.assertEqual(user.telefono, "0303456")

class UsuarioMensajesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("test1", "test@g.com", "12345")
        Usuario(usuario=self.user).save()

    def test_signup_templates_used(self):
        self.client.login(username="test1", password="12345")
        # que usamos el template 'usuarios/inbox_panel.html'
        response = self.client.get(reverse('inbox'))
        self.assertTemplateUsed(response, 'usuarios/inbox_panel.html')

    def test_enviar_mensaje(self):
        user1 = User.objects.create(username='testuser1')
        user1.set_password('12345')
        user1.save()
        user2 = User.objects.create(username='testuser2')
        user2.set_password('12345')
        user2.save()
        self.client.login(username='testuser1', password='12345')
        usuariotest1 = Usuario.objects.create(telefono="333333", direccion="dir_test1", usuario=user1)
        usuariotest2 = Usuario.objects.create(telefono="333332", direccion="dir_test2", usuario=user2)
        response = self.client.post(reverse('inbox'), {
            'texto': 'MensajePrivado',
			'emisor': usuariotest1,
            'receptor': 'testuser2',
			'fecha_envio': timezone.now(),
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/usuarios/inboxPanel")
        self.assertEqual(Mensaje.objects.filter(texto="MensajePrivado").count(), 1)
