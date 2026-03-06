from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    #records
    path('records/', views.record_list, name='record_list'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
    path('records/create/', views.record_create, name='record_create'),
    path('records/<int:pk>/update/', views.record_update, name='record_update'),
    path('records/<int:pk>/delete/', views.record_delete, name='record_delete'),
    #patients
    path('patients/', views.all_patients, name='all_patients'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/history/', views.patient_history, name='patient_history'),
    path('patients/<int:patient_pk>/records/create/', views.medical_record_create, name='medical_record_create'),
    #medical records
    path('medical-records/<int:pk>/', views.medical_record_detail, name='medical_record_detail'),
    path('medical-records/<int:pk>/update/', views.medical_record_update, name='medical_record_update'),
    path('medical-records/<int:pk>/delete/', views.medical_record_delete, name='medical_record_delete'),
    #balances
    path('balances/', views.balance_list, name='balance_list'),
    path('balances/<int:pk>/', views.balance_detail, name='balance_detail'),
    path('balances/create/', views.balance_create, name='balance_create'),
    path('balances/<int:pk>/update/', views.balance_update, name='balance_update'),
    path('balances/<int:pk>/delete/', views.balance_delete, name='balance_delete'),
    path('balances/active-plan/', views.active_plan, name='active_plan'),
]
