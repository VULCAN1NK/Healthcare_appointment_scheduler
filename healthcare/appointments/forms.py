from django import forms
from .models import Appointment, Prescription, Doctor, Patient
from django.contrib.auth.models import User
import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'date', 'time', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'doctor': 'Select Doctor',
            'date': 'Appointment Date',
            'time': 'Appointment Time',
            'reason': 'Reason for Appointment',
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError("The appointment date cannot be in the past.")
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if not time:
            raise forms.ValidationError("You must specify an appointment time.")
        return time

    def save(self, commit=True, patient=None):
        """
        Override save to explicitly set the patient field.
        """
        appointment = super().save(commit=False)
        if patient:
            appointment.patient = patient  # Assign the patient passed from the view
        else:
            raise ValueError("Patient must be provided to save an appointment.")
        if commit:
            appointment.save()
        return appointment

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['doctor', 'patient', 'date', 'notes']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'name', 'specialization', 'phone', 'email']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'name', 'phone', 'email']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
