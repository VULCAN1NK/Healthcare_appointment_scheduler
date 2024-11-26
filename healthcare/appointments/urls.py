# appointments/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('/', views.home, name='home'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('add_prescription/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
    path('view_prescription/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'), 
    path('login/', LoginView.as_view(template_name='appointments/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), 
]
