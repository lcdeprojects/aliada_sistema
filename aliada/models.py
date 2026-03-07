from datetime import datetime, timedelta

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class PatientRecord(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True, help_text="Age in years")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_patients')
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_patients')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='medical_records')
    date = models.DateField()
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    image_medical = models.ImageField(upload_to='medical_records/', blank=True, null=True)
    document = models.FileField(upload_to='medical_records/documents/', blank=True, null=True)
    appointment_feedback = models.TextField(blank=True, null=True, help_text="How was the doctor's appointment?")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_medical_records')
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_medical_records')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Registro para {self.patient.first_name} {self.patient.last_name} em {self.date}"

class BalancePlan(models.Model):
    name = models.CharField(max_length=50)
    expiration_days = models.IntegerField()
    amount = models.FloatField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_balance_plans')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_balance_plans')
    
    def __str__(self):
        return self.name
        
class Balance(models.Model):
    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='balances')
    date = models.DateField()
    type = models.ForeignKey(BalancePlan, on_delete=models.CASCADE, related_name='balances')
    amount = models.FloatField(blank=True, null=True)
    expiration_date = models.DateField(default=None, null=True, blank=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_balances')
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_balances')
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Registro {self.patient.first_name} {self.patient.last_name} em {self.date}"
    
    @property
    def is_expiring_soon(self):
        from datetime import date
        if self.expiration_date:
            days_left = (self.expiration_date - date.today()).days
            return days_left <= 10 and days_left >= 0
        return False
    
    def save(self, *args, **kwargs):
        self.expiration_date = self.date + timedelta(days=self.type.expiration_days) 
        self.amount = self.type.amount     
       
        super().save(*args, **kwargs)

