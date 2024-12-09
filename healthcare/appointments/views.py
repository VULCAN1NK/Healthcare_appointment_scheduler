from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, Prescription, Doctor, Patient
from .forms import AppointmentForm, PrescriptionForm, DoctorSignupForm, PatientSignupForm 
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.contrib.auth.models import Group

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            try:
                # Save the form, which creates both the User and Patient
                patient = form.save()
                user = patient.user  # Get the associated User instance

                # Add the user to the "Patients" group
                patient_group, created = Group.objects.get_or_create(name='Patients')
                patient_group.user_set.add(user)

                return redirect('patient_dashboard')  # Redirect to patient's dashboard
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = PatientSignupForm()
    return render(request, 'signup/patient_signup.html', {'form': form})



def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save doctor data to the database
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard or another page
    else:
        form = DoctorSignupForm()
    return render(request, 'signup/doctor_signup.html', {'form': form})



# Home page (accessible to everyone)
@login_required
def home(request):
    return render(request, 'appointments/home.html')


# Book appointment (accessible only to patients)
@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Fetch the logged-in patient directly
            patient = Patient.objects.filter(user=request.user).first()
            if patient:
                appointment.patient = patient
                appointment.save()
                return redirect('appointment_success')
            else:
                # Add an error if the user is not associated with a Patient
                form.add_error(None, "You must be logged in as a patient to book an appointment.")
        else:
            print(form.errors)
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.groups.filter(name='Patients').exists():
        return redirect('patient_dashboard')
    elif request.user.groups.filter(name='Doctors').exists():
        return redirect('doctor_dashboard')
    else:
        return redirect('home')  # Fallback if no group assigned

# Doctor dashboard (accessible only to doctors)
@login_required
def doctor_dashboard(request):
    try:
        # Ensure the logged-in user is a doctor
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return HttpResponseForbidden("You must be logged in as a doctor to access the dashboard.")

    appointments = Appointment.objects.filter(doctor=doctor)  # Show only the doctor's appointments
    return render(request, 'appointments/doctor_dashboard.html', {'appointments': appointments})


# Patient dashboard (accessible only to patients)
@login_required
def patient_dashboard(request):
    try:
        # Ensure the logged-in user is a patient
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return HttpResponseForbidden("You must be logged in as a patient to access the dashboard.")

    appointments = Appointment.objects.filter(patient=patient)  # Show only the patient's appointments
    return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments})


# Add prescription (accessible only to doctors)
@login_required
def add_prescription(request, appointment_id):
    try:
        # Ensure the logged-in user is a doctor
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return HttpResponseForbidden("You must be logged in as a doctor to add prescriptions.")

    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.doctor = doctor  # Set the doctor to the logged-in user
            prescription.patient = appointment.patient
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'appointments/add_prescription.html', {'form': form, 'appointment': appointment})


# View prescription (accessible only to the patient and the doctor involved)
@login_required
def view_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    if request.user != prescription.doctor.user and request.user != prescription.patient.user:
        return HttpResponseForbidden("You are not authorized to view this prescription.")
    return render(request, 'appointments/view_prescription.html', {'prescription': prescription})


# View the list of patients (accessible only to doctors)
@login_required
def doctor_patients(request):
    try:
        # Ensure the logged-in user is a doctor
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return HttpResponseForbidden("You must be logged in as a doctor to view patients.")

    patients = Patient.objects.all()  # Fetch all patients
    return render(request, 'appointments/doctor_patients.html', {'patients': patients, 'doctor': doctor})


# Appointment success page (accessible to everyone)
def appointment_success(request):
    return render(request, 'appointments/appointment_success.html')


# Logout (accessible to everyone)
def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Redirect to login page after successful signup
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'appointments/signup.html', {'form': form})

def about(request):
    return render(request, 'appointments/about.html')
