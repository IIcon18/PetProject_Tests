from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Articles(models.Model):
    objects = None
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Текст')

    def __str__(self):
        return f':{self.id}'

    def get_absolute_url(self):
        return f'/news/{self.id}'
    class Meta:
        verbose_name = 'Методичка'
        verbose_name_plural = 'Методички'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
