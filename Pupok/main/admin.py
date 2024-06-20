from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Document

# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'  # Изменение множественного числа

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_patronymic', 'get_manager', 'get_position')

    def get_position(self, instance):
        return instance.profile.position if hasattr(instance, 'profile') else None
    get_position.short_description = 'Должность'  # Название колонки

    def get_manager(self, instance):
        return instance.profile.manager if hasattr(instance, 'profile') else None
    get_manager.short_description = 'Руководитель'  # Название колонки

    def get_patronymic(self, instance):
        return instance.profile.patronymic if hasattr(instance, 'profile') else None
    get_patronymic.short_description = 'Отчество'  # Название колонки

# Unregister old User admin
admin.site.unregister(User)

# Register new User admin that includes ProfileInline
admin.site.register(User, UserAdmin)

# Register Document model
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
