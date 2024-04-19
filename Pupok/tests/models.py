from django.db import models

class Articles(models.Model):
    objects = None
    title = models.CharField('Номер', max_length=50)
    anons = models.CharField('Сам вопрос', max_length=250)
    full_text = models.TextField('Варианты ')

    def __str__(self):
        return self.title


