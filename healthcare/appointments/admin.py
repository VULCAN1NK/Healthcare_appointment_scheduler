from django.contrib import admin
from .models import CustomUser, Doctor, Patient, Appointment, Prescription


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')  # Removed username, added relevant fields
    list_filter = ('is_active', 'is_staff')  # Removed user_type
    search_fields = ('email', 'first_name', 'last_name')  # Updated to use the fields from CustomUser
    ordering = ('email',)  # Ordering by email instead of username


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Admin panel for managing Doctor profiles."""
    list_display = ('user', 'specialization', 'phone', 'email')
    search_fields = ('user__email', 'specialization')  # Changed username to email
    ordering = ('user__email',)  # Changed ordering to use email instead of username


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Admin panel for managing Patient profiles."""
    list_display = ('user', 'phone', 'email')
    search_fields = ('user__email',)  # Changed username to email
    ordering = ('user__email',)  # Changed ordering to use email instead of username


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin panel for managing Appointments."""
    list_display = ('doctor', 'patient', 'date', 'time', 'reason')
    list_filter = ('reason', 'date')
    search_fields = ('doctor__user__email', 'patient__user__email')  # Changed username to email
    ordering = ('date', 'time')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """Admin panel for managing Prescriptions."""
    list_display = ('notes', 'doctor', 'patient', 'date')
    search_fields = ('doctor__user__email', 'patient__user__email')  # Changed username to email
    ordering = ('date',)
