from django.conf.urls import include, url
from .views import alquiler_nuevo, home
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', "departamentos.views.home", name='home'),
    url(r'^nuevoAlquiler$', "departamentos.views.alquiler_nuevo", name='alquiler_crear'),
]
