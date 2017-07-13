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


#@login_required()
def home(request):
    contexto = Departamento.objects.all().order_by('id')
    return render_to_response('departamentos/home.html', {'user': request.user, 'alquileres':contexto}, context_instance=RequestContext(request))

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

def alquiler_lista(request):
    user = request.user.usuario
    alquileres = Departamento.objects.filter(usuario=user)
    contexto = {'alquileres':alquileres}
    return render(request, 'departamentos/listado_alquileres_user.html', contexto)

def alquiler_editar(request, id_alquiler):
    alquiler = Departamento.objects.get(id=id_alquiler)
    if request.method == 'GET':
        form = DepartamentoForm(instance=alquiler)
    else:
        form = DepartamentoForm(request.POST, instance=alquiler)
        if form.is_valid():
            form.save()
            messages.success(request, '¡ El alquiler se ha editado correctamente !')
        return redirect('departamentos:alquiler_listado')
    return render(request, 'departamentos/departamento_form.html', {'form':form})

def alquiler_borrar(request, id_alquiler):
    alquiler = Departamento.objects.get(id=id_alquiler)
    if request.method == 'POST':
        alquiler.delete()
        messages.success(request, '¡ El alquiler se ha eliminado correctamente !')
        return redirect('departamentos:alquiler_listado')
    return render(request, 'departamentos/borrado_alquiler.html', {'alquiler':alquiler})
