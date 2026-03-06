from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PatientRecord, MedicalRecord, Balance

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
            'date': forms.DateInput(attrs={'type': 'date'}),
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
        fields = ['patient', 'date', 'type', 'amount', 'description', 'expiration_date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
