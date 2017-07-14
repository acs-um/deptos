from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    url(r'^$', "departamentos.views.home", name='home'),
    url(r'^nuevoAlquiler$', "departamentos.views.alquiler_nuevo", name='alquiler_crear'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registrar/$', 'usuarios.views.signup', name='signup'),
    url(r'^ingresar/$', login, {'template_name': 'usuarios/login.html', }, name="login"),
    url(r'^logout$', logout, {'next_page': '/', }, name="logout"),

    #Reset password
    url(r'^usuarios/reestablecer$', password_reset, {'template_name':'usuarios/reestablecer/password_reset_form.html', 'email_template_name':'usuarios/reestablecer/password_reset_email.html'}, name='password_reset'),
    url(r'^usuarios/reestablecer/notificacion$', password_reset_done, {'template_name':'usuarios/reestablecer/password_reset_done.html'}, name='password_reset_done'),
    url(r'^usuarios/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {'template_name':'usuarios/reestablecer/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^usuarios/reestablecer/finalizado$', password_reset_complete, {'template_name':'usuarios/reestablecer/password_reset_complete.html'}, name='password_reset_complete')
]
