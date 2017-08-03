from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views import generic
from django.utils.translation import gettext_lazy as _

from .forms import SignUpForm, EditPerfil, SetPasswordForm
from .models import Usuario, Mensaje

from django.contrib.auth.views import login

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

class PasswordResetConfirmView(generic.FormView):
    template_name = "usuarios/reestablecer/password_reset_confirm.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    token_generator = default_token_generator
    post_reset_login = False
    post_reset_login_backend = None
    title = _('Enter new password')

    UserModel = get_user_model()
    INTERNAL_RESET_URL_TOKEN = 'reestablecer'
    INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(self.INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[self.INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = self.UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, self.UserModel.DoesNotExist):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[self.INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context
