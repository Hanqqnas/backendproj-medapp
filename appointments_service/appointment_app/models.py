from django.db import models
from django.conf import settings

class Appointment(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"Wizyta: {self.date.strftime('%Y-%m-%d %H:%M')} | Lekarz: {self.doctor.get_full_name()} | Pacjent: {self.patient.get_full_name()}"
