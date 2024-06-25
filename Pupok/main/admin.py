from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Document

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fields = ('phone_number', 'position', 'patronymic', 'is_manager', 'hire_date', 'last_test_date')  # Включаем новые поля

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_patronymic', 'get_position', 'get_is_manager', 'get_hire_date', 'get_last_test_date')

    def get_position(self, instance):
        return instance.profile.position if hasattr(instance, 'profile') else None
    get_position.short_description = 'Должность'

    def get_patronymic(self, instance):
        return instance.profile.patronymic if hasattr(instance, 'profile') else None
    get_patronymic.short_description = 'Отчество'

    def get_is_manager(self, instance):
        return instance.profile.is_manager if hasattr(instance, 'profile') else False
    get_is_manager.short_description = 'Руководитель'

    def get_hire_date(self, instance):
        return instance.profile.hire_date if hasattr(instance, 'profile') else None
    get_hire_date.short_description = 'Дата принятия на работу'

    def get_last_test_date(self, instance):
        return instance.profile.last_test_date if hasattr(instance, 'profile') else None
    get_last_test_date.short_description = 'Последняя дата прохождения теста'

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

# Регистрация моделей в админке
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Document, DocumentAdmin)
