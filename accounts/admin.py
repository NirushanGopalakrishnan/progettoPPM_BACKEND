from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_moderator')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_moderator')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'address', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_moderator', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'address', 'phone', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name', 'address', 'phone')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
