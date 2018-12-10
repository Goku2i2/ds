from django.forms import ModelForm
from django import forms
from .models import Cliente,Orden, Tecnico
from django.contrib.auth.models import User



class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tecnico',
            'nombre',
            'direccion',
            'region',
            'comuna',
            'telefono',
            'correo',
        ]
        widgets = {
            'region':forms.Select,
            'comuna':forms.Select
        }


class TecnicoForm(ModelForm):
    class Meta:
        model=Tecnico
        fields=[
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        widgets = {
        'password': forms.PasswordInput()
        }      
        
          
class OrdenForm(ModelForm):
    class Meta:
        model = Orden
        fields = [
            'fecha',
            'horaInicio',
            'horaTermino',
            'identificadorAscensor',
            'modeloAscensor',
            'fallas',
            'reparaciones',
            'piezas',
            'nombreReceptor',
        ]
        widgets = {
            'fecha': forms.TextInput(attrs={'type': 'date'}),
            'horaInicio': forms.TextInput(attrs={'type': 'time'}),
            'horaTermino': forms.TextInput(attrs={'type': 'time'}),
            }