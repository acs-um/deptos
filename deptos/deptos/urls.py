from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^', include('departamentos.urls', namespace='departamentos')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/', include('usuarios.urls', namespace='usuarios')),
    url(r'^registrar/$', 'usuarios.views.signup', name='signup'),
    url(r'^ingresar/$', login, {'template_name': 'usuarios/login.html', }, name="login"),
]
