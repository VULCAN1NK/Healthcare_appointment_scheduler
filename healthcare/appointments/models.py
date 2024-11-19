from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email



# Doctor model
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'doctor'})
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Nullable field
    email = models.EmailField(default='example@example.com')  # Default value for email

    def __str__(self):
        return self.name


# Patient model
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Nullable field
    email = models.EmailField(default='example@example.com')  # Default value for email

    def __str__(self):
        return self.name


# Appointment model
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.date} at {self.time}"


# Prescription model
class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"Prescription for {self.patient.name} by {self.doctor.name} on {self.date}"
