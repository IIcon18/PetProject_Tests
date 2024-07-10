from django.db import models
import uuid
import random
from django.contrib.auth.models import User

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

class QuestionDifficulty(models.TextChoices):
    EASY = 'easy', 'Легкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'

class Question(BaseModel):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
    ]
    
    gfg = models.ForeignKey(Types, related_name='questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    marks = models.IntegerField(default=5)
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    difficulty = models.CharField(max_length=6, choices=QuestionDifficulty.choices, default=QuestionDifficulty.EASY)
    
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
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.answer

class ExtendedQuestion(BaseModel):
    gfg = models.ForeignKey(Types, related_name='extended_questions', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст вопроса")
    marks = models.IntegerField(default=5)
    image = models.ImageField(upload_to='extended_question_images/', null=True, blank=True)
    difficulty = models.CharField(max_length=6, choices=QuestionDifficulty.choices, default=QuestionDifficulty.EASY)
    
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

class TestResult(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    test_duration = models.DurationField()
    
    @property
    def percentage(self):
        if self.total_questions > 0:
            return (self.correct_answers / self.total_questions) * 100
        return 0

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.correct_answers}/{self.total_questions} ({self.percentage:.2f}%)'
