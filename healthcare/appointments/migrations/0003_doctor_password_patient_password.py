# Generated by Django 5.1.2 on 2024-12-06 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_doctor_email_doctor_phone_doctor_user_patient_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='password',
            field=models.CharField(default='default123', max_length=128),
        ),
        migrations.AddField(
            model_name='patient',
            name='password',
            field=models.CharField(default='default123', max_length=128),
        ),
    ]