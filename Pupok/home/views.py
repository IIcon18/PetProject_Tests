from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *

def home(request):
    categories = Types.objects.all()
    return render(request, 'test/home.html', {'categories': categories})

def quiz(request):
    if request.method == 'GET' and 'gfg' in request.GET:
        selected_category = request.GET.get('gfg')
        questions = Question.objects.filter(gfg__gfg_name__icontains=selected_category)
        return render(request, 'test/quiz.html', {'questions': questions, 'selected_category': selected_category})
    else:
        return redirect('home')

def get_quiz(request):
    try:
        if request.method == 'GET' and 'gfg' in request.GET:
            selected_category = request.GET.get('gfg')
            questions = Question.objects.filter(gfg__gfg_name__icontains=selected_category)
            data = []
            for question in questions:
                answers = list(Answer.objects.filter(question=question))
                data.append({
                    'question': question.question,
                    'answers': [{'answer': answer.answer, 'is_correct': answer.is_correct} for answer in answers]
                })
            payload = {'status': True, 'data': data}
            return JsonResponse(payload)
        else:
            return HttpResponse(status=400)
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong", status=500)

def result(request):
    if request.method == 'POST' and 'gfg' in request.POST:
        selected_category = request.POST.get('gfg')
        questions = Question.objects.filter(gfg__gfg_name__icontains=selected_category)

        total_marks = 0
        correct_answers = 0
        incorrect_answers = 0
        results = []

        for question in questions:
            user_answers = request.POST.getlist(str(question.uid))
            correct = False

            if question.question_type == 'MCQ':
                correct_answers = Answer.objects.filter(question=question, is_correct=True)
                correct_answers_text = [ans.answer for ans in correct_answers]
                if set(user_answers) == set(correct_answers_text):
                    correct = True
            else:  # SA type
                try:
                    extended_question = ExtendedQuestion.objects.get(pk=question.uid)
                    correct_answers_objs = ExtendedAnswer.objects.filter(question=extended_question)
                    for ans in correct_answers_objs:
                        if user_answers and any(user_answer.strip().lower() == ans.text.strip().lower() for user_answer in user_answers):
                            correct = True
                            break
                except ExtendedQuestion.DoesNotExist:
                    pass

            if correct:
                correct_answers += 1
                total_marks += question.marks
            else:
                incorrect_answers += 1

            results.append({
                'question': question.question,
                'user_answers': user_answers,
                'correct': correct
            })

        context = {
            'total_marks': total_marks,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'results': results,
            'selected_category': selected_category
        }
        return render(request, 'test/result.html', context)
    else:
        return redirect('home')

