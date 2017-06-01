from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.test import TestCase


class UrlUsuariosTests(TestCase):

    def test_list(self):
        self.assertEqual(reverse('departamentos:home'), '/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/').view_name, 'departamentos:home')
