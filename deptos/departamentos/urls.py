from django.conf.urls import include, url
from departamentos.views import home

urlpatterns = [
    url(r'^$', "departamentos.views.home", name='home'),
]
