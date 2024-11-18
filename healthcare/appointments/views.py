# appointments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, Prescription
from .forms import AppointmentForm, PrescriptionForm

def home(request):
    return render(request, 'appointments/home.html')

# @login_required
# def book_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.patient = request.user
#             appointment.save()
#             return redirect('appointment_success')
#     else:
#         form = AppointmentForm()
#     return render(request, 'appointments/book_appointment.html', {'form': form})

# # @login_required
# def doctor_dashboard(request):
#     appointments = Appointment.objects.filter(doctor=request.user)
#     return render(request, 'appointments/doctor_dashboard.html', {'appointments': appointments})

# # @login_required
# def patient_dashboard(request):
#     appointments = Appointment.objects.filter(patient=request.user)
#     return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments})

# # @login_required
# def add_prescription(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id)
#     if request.method == 'POST':
#         form = PrescriptionForm(request.POST)
#         if form.is_valid():
#             prescription = form.save(commit=False)
#             prescription.appointment = appointment
#             prescription.doctor = request.user
#             prescription.patient = appointment.patient
#             prescription.save()
#             return redirect('doctor_dashboard')
#     else:
#         form = PrescriptionForm()
#     return render(request, 'appointments/add_prescription.html', {'form': form, 'appointment': appointment})

# # @login_required
# def view_prescription(request, prescription_id):
#     prescription = get_object_or_404(Prescription, id=prescription_id)
#     return render(request, 'appointments/view_prescription.html', {'prescription': prescription})

# def appointment_success(request):
#     return render(request, 'appointments/appointment_success.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')


def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Assuming the patient is the logged-in user. Modify if there's no user linking.
            if request.user.is_authenticated:
                appointment.patient = request.user
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})



    # Doctor dashboard (accessible to everyone)
def doctor_dashboard(request):
    appointments = Appointment.objects.all()  # Show all appointments
    return render(request, 'appointments/doctor_dashboard.html', {'appointments': appointments})

# Patient dashboard (accessible to everyone)
def patient_dashboard(request):
    appointments = Appointment.objects.all()  # Show all appointments
    return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments})

# Add prescription (accessible to everyone)
def add_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            # Assuming logged-in user is the doctor. Modify if no user linking is needed.
            if request.user.is_authenticated:
                prescription.doctor = request.user
            prescription.patient = appointment.patient
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'appointments/add_prescription.html', {'form': form, 'appointment': appointment})

# View prescription (accessible to everyone)
def view_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'appointments/view_prescription.html', {'prescription': prescription})

# Appointment success page (accessible to everyone)
def appointment_success(request):
    return render(request, 'appointments/appointment_success.html')

# Logout (accessible to everyone)
def logout_view(request):
    logout(request)
    return redirect('login')