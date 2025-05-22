from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'description', 'doctor', 'patient']
        read_only_fields = ['patient']