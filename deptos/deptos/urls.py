from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from usuarios.views import PasswordResetConfirmView

urlpatterns = [
    url(r'^$', "departamentos.views.home", name='home'),
    ##ABM ALQUILERES##
    url(r'^nuevoAlquiler$', "departamentos.views.alquiler_nuevo", name='alquiler_crear'),
    url(r'^listadoAlquileres$', "departamentos.views.alquiler_lista", name='alquiler_listado'),
    url(r'^editarArquiler/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_editar", name='alquiler_editar'),
    url(r'^eliminarArquiler/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_borrar", name='alquiler_borrar'),
    url(r'^alquilerEstado/disable/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_disable", name='alquiler_desactivar'),
    url(r'^alquilerEstado/enable/(?P<id_alquiler>\d+)/$', "departamentos.views.alquiler_enable", name='alquiler_activar'),
    url(r'^subirImagen/(?P<id_alquiler>\d+)/$', "departamentos.views.uploadImagen", name='alquiler_subirImagen'),    
    #####FIN-ABM######
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registrar/$', 'usuarios.views.signup', name='signup'),
    url(r'^ingresar/$', login, {'template_name': 'usuarios/login.html', }, name="login"),
    url(r'^logout$', logout, {'next_page': '/', }, name="logout"),
    #Reset password
    url(r'^usuarios/reestablecer$', password_reset, {'template_name':'usuarios/reestablecer/password_reset_form.html', 'email_template_name':'usuarios/reestablecer/password_reset_email.html'}, name='password_reset'),
    url(r'^usuarios/reestablecer/notificacion$', password_reset_done, {'template_name':'usuarios/reestablecer/password_reset_done.html'}, name='password_reset_done'),
    url(r'^usuarios/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^usuarios/reestablecer/finalizado$', password_reset_complete, {'template_name':'usuarios/reestablecer/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^usuarios/perfil$', "usuarios.views.perfil", name="perfil"),
    url(r'^usuarios/inboxPanel$', "usuarios.views.usuario_listadoMensajes", name="inbox"),
    #Detalles Alquiler
    url(r'^details/(?P<pk>\d+)/$', "departamentos.views.details", name='details'),
    url(r'^details/comentario/(?P<pk>\d+)/$', "departamentos.views.details_comentario", name='details_comentario'),
    url(r'^details/mensaje/(?P<pk>\d+)/$', "departamentos.views.details_mensaje", name='details_mensaje'),
]
