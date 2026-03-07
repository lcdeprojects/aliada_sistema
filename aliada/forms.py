from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Balance, BalancePlan, MedicalRecord, PatientRecord


class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['first_name', 'last_name', 'age', 'weight', 'height', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Primeiro Nome', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome', 'required': True}),
            'age': forms.NumberInput(attrs={'min': '0', 'required': False}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'required': False}),
            'height': forms.NumberInput(attrs={'step': '0.1', 'required': False}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'required': False}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefone', 'required': False}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'date', 'description', 'appointment_feedback', 'image_medical', 'weight', 'height', 'document']
        widgets = {
            'patient': forms.Select(attrs={}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'patient': 'Paciente',
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['date', 'type', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'date': 'Data',
            'type': 'Plano',
            'description': 'Descrição',
        }

class BalanceTypeForm(forms.ModelForm):
    class Meta:
        model = BalancePlan
        fields = ['name', 'expiration_days', 'amount', 'medical', 'nutrition', 'percentage_medical', 'percentage_nutrition']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'expiration_days': forms.NumberInput(attrs={'min': '0'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'percentage_medical': forms.NumberInput(attrs={'step': '0.01'}),
            'percentage_nutrition': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': 'Nome',
            'expiration_days': 'Dias de expiração',
            'amount': 'Valor',
            'medical': 'Médico',
            'nutrition': 'Nutrição',
            'percentage_medical': 'Percentual Médico',
            'percentage_nutrition': 'Percentual Nutrição',
        }

