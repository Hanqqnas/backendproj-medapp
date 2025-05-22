from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]  # DODANE!

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


def appointments_page(request):
    return render(request, 'appointment_app/appointments.html')


@login_required
def doctor_appointments_view(request):
    return render(request, 'appointments.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })
