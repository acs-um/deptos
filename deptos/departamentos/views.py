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

##    def form_valid(self, form):
#        departamento = form.save(commit=False)
#        departamento.usuario = self.request.user.usuario
#        departamento.save()
#        messages.success(self.request, 'El alquiler se ha publicado correctamente.')
#        return HttpResponseRedirect(self.success_url) */
