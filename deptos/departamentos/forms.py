from django import forms
from .models import Departamento


class DepartamentoForm(forms.ModelForm):

	class Meta:
		model = Departamento

		fields = [
			'titulo',
			'descripcion',
			'latitud',
			'longitud',
			'capacidad',
			'localidad',
            'precio',
		]
		labels = {
			'titulo': 'Título',
			'descripcion': 'Descripción',
			'latitud': 'Latitud',
			'longitud':'Longitud',
			'capacidad': 'Capacidad',
			'localidad': 'Localidad',
            'precio': 'Precio',
		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un título para su publicación'}),
			'descripcion': forms.Textarea(attrs={'class':'form-control','placeholder': 'Ingrese una descripción lo más detallada posible de su publicación...','rows':4, 'style':'resize:none;'}),
			'latitud': forms.TextInput(attrs={'class':'form-control'}),
			'longitud': forms.TextInput(attrs={'class':'form-control'}),
			'capacidad': forms.Select(attrs={'class':'form-control'}),
			'localidad': forms.Select(attrs={'class':'form-control'}),
			'precio': forms.TextInput(attrs={'class':'form-control'}),
}
