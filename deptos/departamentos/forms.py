from django import forms
from .models import Departamento


class DepartamentoForm(forms.ModelForm):

	class Meta:
		model = Departamento

		fields = [
			'titulo',
			'descripción',
			'latitud',
			'longitud',
			'capacidad',
			'localidad',
            'precio',
		]
		labels = {
			'titulo': 'Título',
			'descripción': 'Descripción',
			'latitud': 'Latitud',
			'longitud':'Longitud',
			'capacidad': 'Capacidad',
			'localidad': 'Localidad',
            'precio': 'Precio',
		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control'}),
			'descripción': forms.TextInput(attrs={'class':'form-control'}),
			'latitud': forms.TextInput(attrs={'class':'form-control'}),
			'longitud': forms.TextInput(attrs={'class':'form-control'}),
			'capacidad': forms.TextInput(attrs={'class':'form-control'}),
			'localidad': forms.TextInput(attrs={'class':'form-control'}),
			'precio': forms.TextInput(attrs={'class':'form-control'}),
}
