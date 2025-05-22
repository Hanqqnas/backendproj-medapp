from appointment_app.models import Appointment
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role',)

    fieldsets = UserAdmin.fieldsets + (
        ('Dodatkowe dane', {'fields': ('role', 'pesel', 'specialization')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dodatkowe dane', {'fields': ('role', 'pesel', 'specialization')}),
    )

admin.site.register(User, CustomUserAdmin)

admin.site.register(Appointment)
