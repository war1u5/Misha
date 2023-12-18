from django.contrib import admin
from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff',
                    'is_commander', 'is_c2operator', 'is_analyst', 'is_agent']
