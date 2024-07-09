from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)

class Choice(models.Model):
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)