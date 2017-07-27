from django.shortcuts import render, render_to_response, redirect
from django.template.context import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import DepartamentoForm
from .models import Departamento


def home(request):
    q = ''
    # capacidad
    c = ''
    # precio
    p = ''
    # localidad
    l = ''
    departamentos = Departamento.objects.all().order_by('id')
    if "q" in request.GET:
        q=request.GET.get("q")
        departamentos = departamentos.filter(descripción__icontains=q)
    if "c" in request.GET and request.GET.get("c") != '':
        c=request.GET.get("c")
        departamentos = departamentos.filter(capacidad=c)
    if "p" in request.GET and request.GET.get("p") != '':
        p=request.GET.get("p")
        departamentos = departamentos.filter(precio=p)
    if "l" in request.GET and request.GET.get("l") != '':
        l=request.GET.get("l")
        departamentos = departamentos.filter(localidad__icontains=l)
    return render_to_response('departamentos/home.html', {'user': request.user, 'alquileres':departamentos}, context_instance=RequestContext(request))

#@login_required()
def alquiler_nuevo(request):
    if request.method == "POST":
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            departamento = form.save(commit=False)
            departamento.usuario = request.user.usuario
            departamento.save()
            messages.success(request, 'El alquiler se ha publicado correctamente.')
            return redirect(reverse('departamentos:home'))
    else:
        form = DepartamentoForm()
    return render(request, 'departamentos/departamento_form.html', {'form': form})

##    def form_valid(self, form):
#        departamento = form.save(commit=False)
#        departamento.usuario = self.request.user.usuario
#        departamento.save()
#        messages.success(self.request, 'El alquiler se ha publicado correctamente.')
#        return HttpResponseRedirect(self.success_url) */
