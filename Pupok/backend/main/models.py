from django.db import models
from django.contrib.auth.models import User
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    is_manager = models.BooleanField(default=False)  # Поле "Руководитель"
    hire_date = models.DateField(blank=True, null=True)  # Дата принятия на работу
    last_test_date = models.DateField(blank=True, null=True)  # Последняя дата прохождения теста

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
