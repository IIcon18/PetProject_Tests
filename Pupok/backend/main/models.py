from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('номер телефона'))
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('должность'))
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('отчество'))
    is_manager = models.BooleanField(default=False, verbose_name=_('руководитель'))
    hire_date = models.DateField(blank=True, null=True, verbose_name=_('дата принятия на работу'))
    last_test_date = models.DateField(blank=True, null=True, verbose_name=_('последняя дата прохождения теста'))

    class Meta:
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')


    def __str__(self):
        return self.user.username

def file_upload_path(instance, filename):
    basename, extension = os.path.splitext(filename)
    truncated_basename = basename[:150]
    return f'documents/{truncated_basename}{extension}'

class Document(models.Model):
    title = models.CharField(max_length=150)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=file_upload_path)

    class Meta:
        verbose_name = "Методичка"
        verbose_name_plural = "Методички"

    def __str__(self):
        return self.title
