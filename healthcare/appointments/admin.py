from django.contrib import admin
from .models import Doctor, Patient, Appointment, Prescription

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone', 'email')
    search_fields = ('user__username', 'specialization')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email')
    search_fields = ('user__username',)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'reason')
    list_filter = ('reason', 'date')
    search_fields = ('doctor__user__username', 'patient__user__username')

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('notes', 'doctor', 'patient', 'date')
    search_fields = ('doctor__user__username', 'patient__user__username')

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
