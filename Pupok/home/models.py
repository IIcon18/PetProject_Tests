from django.db import models
import uuid
import random  # Добавляем импорт модуля random

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True

class Types(BaseModel):
    gfg_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.gfg_name
    
class Question(BaseModel):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('SA', 'Short Answer Question')
    ]
    
    gfg = models.ForeignKey(Types, related_name='gfg', on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=5)
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    
    def __str__(self):
        return self.question
    
    def get_answers(self):
        if self.question_type == 'MCQ':
            answer_objs = list(Answer.objects.filter(question=self))
            data = []
            random.shuffle(answer_objs)
            
            for answer_obj in answer_objs:
                data.append({
                    'answer': answer_obj.answer,
                    'is_correct': answer_obj.is_correct
                })
            return data
        else:
            return []

class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.answer

class ExtendedQuestion(BaseModel):
    text = models.TextField(verbose_name="Текст вопроса")
    
    class Meta:
        verbose_name = "Вопрос с развернутым ответом"
        verbose_name_plural = "Вопросы с развернутым ответом"
    
    def __str__(self):
        return self.text[:50]

class ExtendedAnswer(BaseModel):
    question_text = models.ForeignKey(ExtendedQuestion, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    
    class Meta:
        verbose_name = "Ответ на вопрос с развернутым ответом"
        verbose_name_plural = "Ответы на вопросы с развернутым ответом"
    
    def __str__(self):
        return f"{self.question_text.text[:20]} - {self.text[:50]}"
