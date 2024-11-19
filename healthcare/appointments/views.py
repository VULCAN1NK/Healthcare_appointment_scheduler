from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, Prescription
from .forms import AppointmentForm, PrescriptionForm
from django.urls import reverse

def home(request):
    return render(request, 'appointments/home.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Using request.user (CustomUser)
            appointment.save()
            return redirect('appointment_success.html')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})

@login_required
def doctor_dashboard(request):
    # Make sure 'doctor' field refers to 'CustomUser' model
    appointments = Appointment.objects.filter(doctor=request.user)  # 'request.user' is a CustomUser
    return render(request, 'appointments/doctor_dashboard.html', {'appointments': appointments})

@login_required
def patient_dashboard(request):
    # Make sure 'patient' field refers to 'CustomUser' model
    appointments = Appointment.objects.filter(patient=request.user)  # 'request.user' is a CustomUser
    return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments})

@login_required
def add_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.doctor = request.user  # Assigning the current user as doctor
            prescription.patient = appointment.patient
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'appointments/add_prescription.html', {'form': form, 'appointment': appointment})

@login_required
def view_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'appointments/view_prescription.html', {'prescription': prescription})

def appointment_success(request):
    return render(request, 'appointments/appointment_success.html')

def logout_view(request):
    logout(request)
    return redirect('login.html')

def user_selection(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'doctor':
            return redirect(reverse('doctor_dashboard'))
        elif user_type == 'patient':
            return redirect(reverse('patient_dashboard'))
    return render(request, 'appointment/user_selection.html')
