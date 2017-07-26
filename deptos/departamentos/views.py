from django.shortcuts import render, render_to_response, redirect
from django.template.context import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import DepartamentoForm, ComentarioForm
from .models import Departamento, Foto

import datetime

def home(request):
    q = ''
    if "q" in request.GET:
        q=request.GET.get("q")
        contexto=Departamento.objects.filter(descripcion__icontains=q)
    else:
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
            return redirect(reverse('home'))
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
            messages.success(request, 'El alquiler se ha editado correctamente !')
        return redirect('alquiler_listado')
    return render(request, 'departamentos/departamento_form_edit.html', {'form':form})

def alquiler_borrar(request, id_alquiler):
    alquiler = Departamento.objects.get(id=id_alquiler)
    if request.method == 'POST':
        alquiler.delete()
        messages.success(request, 'El alquiler se ha eliminado correctamente !')
        return redirect('alquiler_listado')
    return render(request, 'departamentos/borrado_alquiler.html', {'alquiler':alquiler})


def alquiler_disable(request, id_alquiler):
    alquiler = Departamento.objects.get(id=id_alquiler)
    alquiler.estado = False
    alquiler.save()
    messages.success(request, 'El alquiler se ha desactivado correctamente. No estará disponible en la página principal hasta que lo active nuevamente.')
    return redirect(reverse('alquiler_listado'))

def alquiler_enable(request, id_alquiler):
    alquiler = Departamento.objects.get(id=id_alquiler)
    alquiler.estado = True
    alquiler.save()
    messages.success(request, 'El alquiler se ha activado correctamente. Ahora está disponible en la página principal y será visible para todos.')
    return redirect(reverse('alquiler_listado'))

def details(request, pk):
    depto = Departamento.objects.get(pk=pk)
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.emisor = request.user.usuario
            comentario.fecha_envio = datetime.datetime.now()
            comentario.departamento = depto
            comentario.save()
            messages.success(request, 'El comentario se ha publicado correctamente.')
            return redirect(reverse('details', args=[pk]))
    else:
        form = ComentarioForm()
    return render(request, 'departamentos/details.html', {'user': request.user, 'depto': Departamento.objects.get(pk=pk), 'form': form})
