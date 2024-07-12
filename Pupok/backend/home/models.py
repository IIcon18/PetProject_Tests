from django.db import models
import uuid
import random
from django.contrib.auth.models import User

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name="UUID")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        abstract = True

class Types(BaseModel):
    gfg_name = models.CharField(max_length=100, verbose_name="Название типа")
    
    def __str__(self):
        return self.gfg_name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class QuestionDifficulty(models.TextChoices):
    EASY = 'easy', 'Легкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'

class Question(BaseModel):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
    ]
    
    gfg = models.ForeignKey(Types, related_name='questions', on_delete=models.CASCADE, verbose_name="Тип")
    question = models.CharField(max_length=250, verbose_name="Вопрос")
    marks = models.IntegerField(default=5, verbose_name="Баллы")
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPE_CHOICES, default='MCQ', verbose_name="Тип вопроса")
    image = models.ImageField(upload_to='question_images/', null=True, blank=True, verbose_name="Изображение")
    difficulty = models.CharField(max_length=6, choices=QuestionDifficulty.choices, default=QuestionDifficulty.EASY, verbose_name="Сложность")
    
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

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.CharField(max_length=200, verbose_name="Ответ")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    
    def __str__(self):
        return self.answer
    
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

class ExtendedQuestion(BaseModel):
    gfg = models.ForeignKey(Types, related_name='extended_questions', on_delete=models.CASCADE, verbose_name="Тип")
    text = models.TextField(verbose_name="Текст вопроса")
    marks = models.IntegerField(default=5, verbose_name="Баллы")
    image = models.ImageField(upload_to='extended_question_images/', null=True, blank=True, verbose_name="Изображение")
    difficulty = models.CharField(max_length=6, choices=QuestionDifficulty.choices, default=QuestionDifficulty.EASY, verbose_name="Сложность")
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    correct_answers = models.IntegerField(verbose_name="Правильные ответы")
    total_questions = models.IntegerField(verbose_name="Всего вопросов")
    test_duration = models.DurationField(verbose_name="Длительность теста")
    
    @property
    def percentage(self):
        if self.total_questions > 0:
            return (self.correct_answers / self.total_questions) * 100
        return 0

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.correct_answers}/{self.total_questions} ({self.percentage:.2f}%)'
    
    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
