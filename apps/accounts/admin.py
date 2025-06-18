from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User  # замени путь, если нужно


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_active', 'is_staff', 'account_type')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff')}),
        (_('Account'), {'fields': ('account_type',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'account_type', 'is_active', 'is_staff'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)




