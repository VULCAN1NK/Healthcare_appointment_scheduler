from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Nullable field
    email = models.EmailField(default='example@example.com')  # Default value for email

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')  # Default value for email
    phone = models.CharField(max_length=15, null=True, blank=True)  # Nullable field

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()  # Ensured reason field is included

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time}"

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"Prescription for {self.patient} by Dr. {self.doctor.name} on {self.date}"
