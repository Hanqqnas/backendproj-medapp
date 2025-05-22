from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from .views import doctor_appointments_view

from .views import whoami_view

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
app_name = 'appointments'
urlpatterns = [
    path('', include(router.urls)),
    path('my-appointments/', doctor_appointments_view, name='my-appointments'),
    path('whoami/', whoami_view, name='whoami'),
]
