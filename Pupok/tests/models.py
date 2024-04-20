from django.db import models

class Questions(models.Model):
    objects = None
    number = models.CharField('Номер', max_length=50)
    anons = models.CharField('Сам вопрос', max_length=250)
    full_text = models.TextField('Варианты ')

    def __str__(self):
        return self.number


