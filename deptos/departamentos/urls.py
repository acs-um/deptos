from django.conf.urls import include, url
from .views import alquiler_nuevo, home, alquiler_lista, alquiler_editar, alquiler_borrar
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', "departamentos.views.home", name='home'),
    url(r'^nuevoAlquiler$', "departamentos.views.alquiler_nuevo", name='alquiler_crear'),
    url(r'^listadoAlquileres$', "departamentos.views.alquiler_lista", name='alquiler_listado'),
    url(r'^editarArquiler/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_editar", name='alquiler_editar'),
    url(r'^eliminarArquiler/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_borrar", name='alquiler_borrar'),
]
