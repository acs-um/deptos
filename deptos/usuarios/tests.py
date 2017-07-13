from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User

from django.test import TestCase

from .forms import SignUpForm
from .models import Usuario


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
            'username': "test",
            'password': "123123",
            'email': "test@g.com",
            'first_name': "Test",
            'last_name': "Last name"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/ingresar/")

        #Se comprueba que haya sido creado en la tabla User
        self.assertEqual(User.objects.filter(username="test").count(), 1)

        #Se comprueba que haya sido creado en la tabla Usuario
        self.assertEqual(Usuario.objects.filter(usuario__username="test").count(), 1)

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
