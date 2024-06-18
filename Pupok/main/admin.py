from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'  # Изменение множественного числа

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_position', 'get_manager')

    def get_position(self, instance):
        return instance.profile.position if hasattr(instance, 'profile') else None
    get_position.short_description = 'Должность'  # Название колонки

    def get_manager(self, instance):
        return instance.profile.manager if hasattr(instance, 'profile') else None
    get_manager.short_description = 'Руководитель'  # Название колонки

# Unregister old User admin
admin.site.unregister(User)

# Register new User admin that includes ProfileInline
admin.site.register(User, UserAdmin)
