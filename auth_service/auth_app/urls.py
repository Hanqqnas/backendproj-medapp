from django.urls import path
from auth_app.views import register_view, login_view, doctor_dashboard, patient_dashboard, logout_view, doctors_list_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import CustomTokenObtainPairSerializer, CurrentUserView
from auth_app.views import home_view
from auth_app.views import book_visit_view
from .views import CurrentUserView

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('api/login/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('logout/', logout_view, name='logout'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctors/', doctors_list_view, name='doctors_list'),
    path('book/', book_visit_view, name='book_visit'),

    path('api/register/', register_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', CurrentUserView.as_view(), name='current_user'),
]
