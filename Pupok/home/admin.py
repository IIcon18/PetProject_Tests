from django.contrib import admin
from .models import *

class AnswerAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    list_display = ('question', 'gfg', 'marks', 'question_type')
    search_fields = ('question',)
    list_filter = ('gfg', 'question_type')
    fields = ('question', 'gfg', 'marks', 'question_type', 'image')  # Добавлено поле 'image'

class ExtendedAnswerAdmin(admin.StackedInline):
    model = ExtendedAnswer

class ExtendedQuestionAdmin(admin.ModelAdmin):
    inlines = [ExtendedAnswerAdmin]
    list_display = ('text', 'gfg', 'marks')
    search_fields = ('text',)
    list_filter = ('gfg',)

admin.site.register(Types)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(ExtendedQuestion, ExtendedQuestionAdmin)
admin.site.register(ExtendedAnswer)
