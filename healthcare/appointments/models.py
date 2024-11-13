from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Appointments(models.Model):
     doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
     patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
     date = models.DateField()
     time = models.TimeField()

     def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.date} at {self.time}"