from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from .forms import SignUpForm, EditPerfil
from .models import Usuario, Mensaje

@login_required
def perfil(request):

    if request.method == 'POST':
        form = EditPerfil(request.POST, instance=request.user)
        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.get(id=request.user.id)
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            customUser = Usuario.objects.get(usuario=user)
            customUser.direccion = request.POST["direccion"]
            customUser.telefono = request.POST["telefono"]
            customUser.save()

            user.save()

            return HttpResponseRedirect(reverse("perfil"))
    else:
        form = EditPerfil(instance=request.user)

    usuario = Usuario.objects.get(usuario__username=request.user.username)

    data = {
        'form': form,
        'usuario': usuario
    }

    return render_to_response('usuarios/datos_usuario.html', data, context_instance=RequestContext(request))

def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = SignUpForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass

            # Process the data in form.cleaned_data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            # At this point, user is a User object that has already been saved
            # to the database. You can continue to change its attributes
            # if you want to change other fields.
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            # Save new user attributes
            user.save()

            usuario = Usuario(usuario = user)
            usuario.direccion = ""
            usuario.telefono = ""
            usuario.save()

            return HttpResponseRedirect("/ingresar/")  # Redirect after POST
    else:
        form = SignUpForm()
    data = {
        'form': form,
    }

    return render_to_response('usuarios/signup.html', data, context_instance=RequestContext(request))

def usuario_listadoMensajes(request):
    mensajes = Mensaje.objects.all().order_by('fecha_envio').reverse()
    return render(request, 'usuarios/inbox_panel.html', { 'mensajes': mensajes, 'user': request.user })
