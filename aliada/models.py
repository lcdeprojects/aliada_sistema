from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class PatientRecord(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True, help_text="Age in years")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_patients')
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_patients')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient: {self.first_name} {self.last_name}"


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
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_medical_records')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.patient.first_name} {self.patient.last_name} on {self.date}"

