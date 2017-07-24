from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm

class SignUpForm(ModelForm):
    username = forms.CharField(min_length=5)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(min_length=5, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def clean_password_confirmation(self):
        if self.data['password'] != self.data['password_confirmation']:
            raise forms.ValidationError('La contraseña no coincide')
        return self.data['password']

    def clean_email(self):
        user = User.objects.filter(email=self.data['email'])
        if user.exists():
            raise forms.ValidationError('Ya existe un usuario con ese email')
        return self.data['email']

class EditPerfil(UserChangeForm):
    username = forms.CharField(min_length=5)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def clean_email(self):
        user = User.objects.filter(email=self.data['email']).exclude(id=self.instance.id)
        if user.exists():
            raise forms.ValidationError('Ya existe un usuario con ese email')
        return self.data['email']
