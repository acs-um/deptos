from django.shortcuts import render, render_to_response, redirect
from django.template.context import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import DepartamentoForm, ComentarioForm, UploadImageForm
from .models import Departamento, Foto

import datetime

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
        departamentos = departamentos.filter(descripcion__icontains=q)
    if "c" in request.GET and request.GET.get("c") != '':
        c=request.GET.get("c")
        departamentos = departamentos.filter(capacidad=c)
    if "p" in request.GET and request.GET.get("p") != '':
        p=request.GET.get("p")
        departamentos = departamentos.filter(precio__range=(0.0,p))
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
    return render(request, 'departamentos/departamento_form_edit.html', {'form':form, 'alquiler':alquiler})

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

def uploadImagen(request, id_alquiler):
    if(Foto.objects.filter(departamento_id=id_alquiler).count() == 5):
        messages.success(request,'No puedes subir más imagenes. Has alcanzado el máximo de fotos para tu publicación (5 máx.)')
        return redirect('alquiler_listado')
    alquiler = Departamento.objects.get(id=id_alquiler)
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.departamento=alquiler
            form.save()
            messages.success(request, 'La imagen se ha subido correctamente.')
            return redirect('alquiler_listado')
    else:
        form = UploadImageForm()
    return render_to_response('departamentos/uploadImagen.html', locals(), context_instance=RequestContext(request))
