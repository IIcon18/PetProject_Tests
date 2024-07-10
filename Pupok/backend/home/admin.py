from django.contrib import admin
from .models import *

class AnswerAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    list_display = ('question', 'gfg', 'marks', 'question_type', 'difficulty')
    search_fields = ('question',)
    list_filter = ('gfg', 'question_type', 'difficulty')
    fields = ('question', 'gfg', 'marks', 'question_type', 'image', 'difficulty')

class ExtendedAnswerAdmin(admin.StackedInline):
    model = ExtendedAnswer

class ExtendedQuestionAdmin(admin.ModelAdmin):
    inlines = [ExtendedAnswerAdmin]
    list_display = ('text', 'gfg', 'marks', 'difficulty')
    search_fields = ('text',)
    list_filter = ('gfg', 'difficulty')

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'correct_answers', 'total_questions', 'percentage', 'test_duration', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('created_at',)
    
    def percentage(self, obj):
        return f"{obj.percentage:.2f}%"
    percentage.short_description = 'Percentage'

admin.site.register(Types)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(ExtendedQuestion, ExtendedQuestionAdmin)
admin.site.register(ExtendedAnswer)
admin.site.register(TestResult, TestResultAdmin)
