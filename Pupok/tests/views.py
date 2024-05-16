from django.shortcuts import render, redirect
from .models import Question, Choice

def index(request):
    questions = Question.objects.all()
    return render(request, 'test/index1.html', {'questions': questions})

def submit_answers(request):
    if request.method == 'POST':
        score = 0
        for question_id, selected_choice_id in request.POST.items():
            if question_id.isdigit():
                question = Question.objects.get(pk=question_id)
                selected_choice = Choice.objects.get(pk=selected_choice_id)
                if selected_choice.is_correct:
                    score += 1
        total_questions = Question.objects.count()
        percentage_score = (score / total_questions) * 100
        return render(request, 'test/result.html', {'score': score, 'total_questions': total_questions, 'percentage_score': percentage_score})
    else:
        return redirect('index1')

