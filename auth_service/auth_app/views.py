import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, RegisterSerializer
from appointment_app.models import Appointment
from appointment_app.serializers import AppointmentSerializer

User = get_user_model()

# === API ===

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("Użytkownik:", self.request.user)  # DEBUG
        serializer.save(patient=self.request.user)



# === WIDOKI HTML ===

SPECIALIZATIONS = [
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

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        pesel = request.POST.get('pesel')
        specialization = request.POST.get('specialization')

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name,
            pesel=pesel if role == 'patient' else None,
            specialization=specialization if role == 'doctor' else None,
        )

        try:
            requests.post("http://127.0.0.1:8001/api/sync-user/", json={
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "pesel": user.pesel,
                "specialization": user.specialization,
            })
        except Exception as e:
            print("SYNC FAILED:", e)

        return redirect('login')

    return render(request, 'auth_app/register.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)

            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            return redirect('patient_dashboard')

        return render(request, 'login.html', {'error': 'Nieprawidłowe dane logowania'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def doctor_dashboard(request):
    visits = Appointment.objects.filter(doctor=request.user).order_by('date')
    return render(request, 'doctor_dashboard.html', {'visits': visits})

@login_required
def patient_dashboard(request):
    visits = Appointment.objects.filter(patient=request.user).order_by('date')
    return render(request, 'patient_dashboard.html', {'visits': visits})
@login_required
def doctors_list_view(request):
    specialization = request.GET.get('specialization')
    doctors = User.objects.filter(role='doctor')
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    return render(request, 'doctors_list.html', {
        'doctors': doctors,
        'specializations': SPECIALIZATIONS,
        'selected': specialization
    })

@login_required
def book_visit_view(request):
    doctors = User.objects.filter(role='doctor')

    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        doctor_id = request.POST.get('doctor')

        access_token = request.session.get('access_token')
        headers = {"Authorization": f"Bearer {access_token}"}

        payload = {
            "date": date,
            "description": description,
            "doctor": doctor_id
        }

        try:
            response = requests.post("http://127.0.0.1:8001/api/appointments/", json=payload, headers=headers)
            response.raise_for_status()
            return render(request, 'auth_app/book_visit.html', {
                'doctors': doctors,
                'success': 'Wizyta została zapisana!'
            })
        except requests.exceptions.HTTPError:
            return render(request, 'auth_app/book_visit.html', {
                'doctors': doctors,
                'error': f"Błąd: {response.status_code} - {response.text}"
            })
        except Exception as e:
            return render(request, 'auth_app/book_visit.html', {
                'doctors': doctors,
                'error': f"Błąd systemu: {str(e)}"
            })

    return render(request, 'auth_app/book_visit.html', {'doctors': doctors})
