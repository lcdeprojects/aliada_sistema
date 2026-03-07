# Create your views here.
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    BalanceForm,
    MedicalRecordForm,
    PatientRecordForm,
    UserRegistrationForm,
)
from .groups import group_required
from .models import Balance, BalancePlan, MedicalRecord, PatientRecord


def home(request):
    context = {}
    if request.user.is_authenticated:
        from django.utils import timezone
        today = timezone.now().date()
        context['patients_count'] = PatientRecord.objects.count()
        context['records_count'] = MedicalRecord.objects.count()
        context['today_records'] = MedicalRecord.objects.filter(date=today).count()
    return render(request, 'core/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

@group_required('Administrador')
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@group_required('admin')
def record_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'first_name')  # Default sort by first_name
    records = PatientRecord.objects.all()
    if query:
        records = records.filter(
            models.Q(first_name__icontains=query) | models.Q(last_name__icontains=query)
        )
    records = records.order_by(sort_by)
    paginator = Paginator(records, 6)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/patient/record_list.html', {'page_obj': page_obj, 'query': query, 'sort_by': sort_by})

@group_required('admin')
def record_detail(request, pk):
    record = get_object_or_404(PatientRecord, pk=pk)
    # Get previous and next records by pk
    prev_record = PatientRecord.objects.filter(pk__lt=record.pk).order_by('-pk').first()
    next_record = PatientRecord.objects.filter(pk__gt=record.pk).order_by('pk').first()
    return render(request, 'core/patient/record_detail.html', {'record': record, 'prev_record': prev_record, 'next_record': next_record})

@login_required
def record_create(request):
    if request.method == 'POST':
        form = PatientRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.save()
            return redirect('record_list')
    else:
        form = PatientRecordForm()
    return render(request, 'core/patient/record_form.html', {'form': form, 'title': 'Create Record'})

@login_required
def record_update(request, pk):
    record = get_object_or_404(PatientRecord, pk=pk)
    if request.method == 'POST':
        form = PatientRecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.updated_by = request.user
            record.save()
            return redirect('record_detail', pk=record.pk)
    else:
        form = PatientRecordForm(instance=record)
    return render(request, 'core/patient/record_form.html', {'form': form, 'title': 'Update Record'})

@group_required('admin')
def patient_detail(request, pk):
    patient = get_object_or_404(PatientRecord, pk=pk)
    medical_records = patient.medical_records.all().order_by('-date')
    return render(request, 'core/patient/patient_detail.html', {'patient': patient, 'medical_records': medical_records})

@login_required
def record_delete(request, pk):
    record = get_object_or_404(PatientRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')
    return render(request, 'core/patient/record_confirm_delete.html', {'record': record})

@group_required('admin')
def medical_record_create(request, patient_pk):
    patient = get_object_or_404(PatientRecord, pk=patient_pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.created_by = request.user
            record.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = MedicalRecordForm(initial={'patient': patient})
    return render(request, 'core/medical/medical_record_form.html', {'form': form, 'title': 'Create Medical Record', 'patient': patient})

@login_required
def medical_record_detail(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'core/medical/medical_record_detail.html', {'record': record})

@login_required
def medical_record_update(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.updated_by = request.user
            record.save()
            return redirect('medical_record_detail', pk=record.pk)
    else:
        form = MedicalRecordForm(instance=record)
    return render(request, 'core/medical/medical_record_form.html', {'form': form, 'title': 'Update Medical Record', 'patient': record.patient})

@login_required
def medical_record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('patient_detail', pk=record.patient.pk)

@login_required
def patient_history(request, pk):
    patient = get_object_or_404(PatientRecord, pk=pk)
    medical_records = patient.medical_records.all().order_by('-date')
    return render(request, 'core/patient/patient_history.html', {'patient': patient, 'medical_records': medical_records})
    
#BAL
@group_required('Administrador')
def balance_create(request):
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            balance = form.save(commit=False)
            patient_id = request.POST.get('patient')
            if patient_id:
                balance.patient_id = int(patient_id)
            balance.created_by = request.user
            balance.save()
            return redirect('balance_list')
    else:
        form = BalanceForm()
    patients = PatientRecord.objects.all()
    return render(request, 'core/balance/balance_form.html', {'form': form, 'title': 'Criar Registro Financeiro', 'patients': patients})

@group_required('Administrador')
def balance_list(request):
    query = request.GET.get('q', '')
    query2 = request.GET.get('q2', '')
    balances = Balance.objects.all()
    if query and query2:
        balances = balances.filter(date__range=[query, query2])
    elif query:
        balances = balances.filter(date__gte=query)
    balances = balances.order_by('-date')
    total = balances.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'core/balance/balance_list.html', {'balances': balances, 'query': query, 'query2': query2, 'total': total})

@group_required('Administrador')
def balance_detail(request, pk):
    balance = get_object_or_404(Balance, pk=pk)
    return render(request, 'core/balance/balance_detail.html', {'balance': balance})

@group_required('Administrador')
def balance_update(request, pk):
    balance = get_object_or_404(Balance, pk=pk)
    if request.method == 'POST':
        form = BalanceForm(request.POST, instance=balance)
        if form.is_valid():
            balance = form.save(commit=False)
            patient_id = request.POST.get('patient')
            if patient_id:
                balance.patient_id = int(patient_id)
            balance.updated_by = request.user
            balance.save()
            return redirect('balance_detail', pk=balance.pk)
    else:
        form = BalanceForm(instance=balance)
    patients = PatientRecord.objects.all()
    return render(request, 'core/balance/balance_form.html', {'form': form, 'title': 'Update Balance', 'patients': patients})

@group_required('Administrador')
def balance_delete(request, pk):
    balance = get_object_or_404(Balance, pk=pk)
    if request.method == 'POST':
        balance.delete()
        return redirect('balance_list')
    return render(request, 'core/balance/balance_confirm_delete.html', {'balance': balance})


@group_required('Administrador')
def sum_balances(request):
    balances = Balance.objects.all()
    total = balances.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'core/balance/sum_balances.html', {'balances': balances, 'total': total})

@group_required('Administrador', 'Secretaria')
def all_patients(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'first_name')  # Default sort by first_name
    records = PatientRecord.objects.all()
    if query:
        records = records.filter(
            models.Q(first_name__icontains=query) | models.Q(last_name__icontains=query)
        )
    records = records.order_by(sort_by)
    paginator = Paginator(records, 4)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/all_patients.html', {'page_obj': page_obj, 'query': query, 'sort_by': sort_by})

@group_required('Administrador', 'Secretaria')
def active_plan(request):
    status = request.GET.get('status', 'active')
    balances = Balance.objects.all()
    if status == 'active':
        balances = balances.filter(active=True)
    elif status == 'inactive':
        balances = balances.filter(active=False)
    elif status == 'expiring':
        today = date.today()
        end_date = today + timedelta(days=10)
        balances = balances.filter(
            expiration_date__gte=today,
            expiration_date__lte=end_date,
            active=True
        )
    balances = balances.order_by('-date')
    return render(request, 'core/balance/active_plan.html', {'balances': balances, 'status': status})

@csrf_exempt
def balance_plans_api(request):
    """API endpoint to get BalancePlan data for the form"""
    if request.method == 'GET':
        plans = BalancePlan.objects.all()
        data = {}
        for plan in plans:
            data[str(plan.id)] = {
                'name': plan.name,
                'amount': plan.amount,
                'expiration_days': plan.expiration_days
            }
        return JsonResponse(data)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@group_required('Administrador')
def balance_plan_menu(request):
    """BalancePlan management menu with statistics and recent activity"""
    from django.db.models import Avg
    from django.utils import timezone
    
    plans = BalancePlan.objects.all()
    
    # Calculate statistics
    stats = {
        'total_plans': plans.count(),
        'avg_amount': plans.aggregate(Avg('amount'))['amount__avg'] or 0,
        'avg_expiration': plans.aggregate(Avg('expiration_days'))['expiration_days__avg'] or 0,
    }
    
    # Mock recent activity (you can customize this based on your needs)
    recent_activities = []
    for plan in plans.order_by('-pk')[:5]:
        recent_activities.append({
            'title': f'Plano "{plan.name}" criado/alterado',
            'icon': 'edit',
            'time': plan.updated_at if hasattr(plan, 'updated_at') else timezone.now()
        })
    
    context = {
        'total_plans': plans.count(),
        'stats': stats,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'core/balance_plan/balance_plan_menu.html', context)

@group_required('Administrador')
def balance_plan_list(request):
    """List all BalancePlans"""
    plans = BalancePlan.objects.all()
    return render(request, 'core/balance_plan/balance_plan_list.html', {'plans': plans})

@group_required('Administrador')
def balance_plan_create(request):
    """Create a new BalancePlan"""
    if request.method == 'POST':
        from .forms import BalanceTypeForm
        form = BalanceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plano de saldo criado com sucesso!')
            return redirect('balance_plan_list')
    else:
        from .forms import BalanceTypeForm
        form = BalanceTypeForm()
    return render(request, 'core/balance_plan/balance_plan_form.html', {'form': form, 'title': 'Criar Plano de Saldo'})

@group_required('Administrador')
def balance_plan_update(request, pk):
    """Update an existing BalancePlan"""
    plan = get_object_or_404(BalancePlan, pk=pk)
    if request.method == 'POST':
        from .forms import BalanceTypeForm
        form = BalanceTypeForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plano de saldo atualizado com sucesso!')
            return redirect('balance_plan_list')
    else:
        from .forms import BalanceTypeForm
        form = BalanceTypeForm(instance=plan)
    return render(request, 'core/balance_plan/balance_plan_form.html', {'form': form, 'title': 'Editar Plano de Saldo'})

@group_required('Administrador')
def balance_plan_delete(request, pk):
    """Delete a BalancePlan"""
    plan = get_object_or_404(BalancePlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plano de saldo excluído com sucesso!')
        return redirect('balance_plan_list')
    return render(request, 'core/balance_plan/balance_plan_confirm_delete.html', {'plan': plan})