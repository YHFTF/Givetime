from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'nickname', 'exp', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인정보', {'fields': ('nickname', 'location', 'profile_image', 'about', 'skills', 'services', 'exp')}),
        ('권한', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'nickname')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
