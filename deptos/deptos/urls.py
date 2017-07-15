from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', "departamentos.views.home", name='home'),
    ##ABM ALQUILERES##
    url(r'^nuevoAlquiler$', "departamentos.views.alquiler_nuevo", name='alquiler_crear'),
    url(r'^listadoAlquileres$', "departamentos.views.alquiler_lista", name='alquiler_listado'),
    url(r'^editarArquiler/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_editar", name='alquiler_editar'),
    url(r'^eliminarArquiler/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_borrar", name='alquiler_borrar'),
    #####FIN-ABM######
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registrar/$', 'usuarios.views.signup', name='signup'),
    url(r'^ingresar/$', login, {'template_name': 'usuarios/login.html', }, name="login"),
    url(r'^logout$', logout, {'next_page': '/', }, name="logout"),
]
