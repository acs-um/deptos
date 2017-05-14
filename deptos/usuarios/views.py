from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.template.loader import get_template

from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'usuarios/home.html')
