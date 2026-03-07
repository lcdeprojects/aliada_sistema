from django.contrib import admin

# Register your models here.
from .models import Balance, BalancePlan, MedicalRecord, PatientRecord


@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'age', 'weight', 'height', 'created_at']
    search_fields = ['first_name', 'last_name']
    list_filter = ['created_at']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'description', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'description']
    list_filter = ['date', 'created_at']

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'type', 'amount', 'description', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'type', 'description']
    list_filter = ['date', 'type', 'created_at']

@admin.register(BalancePlan)
class BalancePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'expiration_days', 'amount']
    search_fields = ['name']
    list_filter = ['expiration_days', 'amount']

