from django.contrib import admin

from authentication.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Avatar image', {'fields': ('avatar_img',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'avatar_img',),
        }),
    )


admin.site.register(User, CustomUserAdmin)
