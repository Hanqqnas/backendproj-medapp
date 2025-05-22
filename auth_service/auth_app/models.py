from django.contrib.auth.models import AbstractUser
from django.db import models

SPECIALIZATION_CHOICES = [
    ('orthopedist', 'Orthopedist'),
    ('neurologist', 'Neurologist'),
    ('family_doctor', 'Family Doctor'),
    ('ophthalmologist', 'Ophthalmologist'),
    ('otolaryngologist', 'Otolaryngologist'),
    ('dermatologist', 'Dermatologist'),
    ('gynecologist', 'Gynecologist'),
    ('pediatrician', 'Pediatrician'),
    ('psychiatrist', 'Psychiatrist'),
]

specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True, null=True)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    pesel = models.CharField(max_length=11, blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"