from django.shortcuts import render, redirect
from .models import Question, Answer
from .forms import TestForm

def test_view(request):
    if request.method == 'POST':
        form = TestForm(request.POST, questions=Question.objects.all())
        if form.is_valid():
            for question_id, answer_text in form.cleaned_data.items():
                question = Question.objects.get(id=question_id)
                Answer.objects.create(question=question, text=answer_text)
            return redirect('result')
    else:
        form = TestForm(questions=Question.objects.all())
    return render(request, 'main/test.html', {'form': form})

def result_view(request):
    answers = Answer.objects.all()
    return render(request, 'main/result.html', {'answers': answers})
