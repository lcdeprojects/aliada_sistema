from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PatientRecord, MedicalRecord

class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['first_name', 'last_name', 'age', 'weight', 'height']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Primeiro Nome', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome', 'required': True}),
            'age': forms.NumberInput(attrs={'min': '0', 'required': True}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'required': True}),
            'height': forms.NumberInput(attrs={'step': '0.1', 'required': True}),
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


