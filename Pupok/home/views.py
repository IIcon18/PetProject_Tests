from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import *
import random
from datetime import datetime, timedelta

def home(request):
    return render(request, 'test/home.html')

def quiz(request):
    start_time = timezone.now()  # Сохранение времени начала теста
    request.session['start_time'] = start_time.isoformat()

    questions = list(Question.objects.all())
    extended_questions = list(ExtendedQuestion.objects.all())

    return render(request, 'test/quiz.html', {'questions': questions, 'extended_questions': extended_questions})

def get_quiz(request):
    try:
        questions = Question.objects.all()
        data = []
        for question in questions:
            answers = list(Answer.objects.filter(question=question))
            data.append({
                'uid': str(question.uid),
                'question': question.question,
                'marks': question.marks,
                'question_type': question.question_type,
                'answers': [{'answer': answer.answer, 'is_correct': answer.is_correct} for answer in answers]
            })
        payload = {'status': True, 'data': data}
        return JsonResponse(payload)
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong", status=500)

def result(request):
    if request.method == 'POST':
        questions = list(Question.objects.all())
        extended_questions = list(ExtendedQuestion.objects.all())

        # Получение времени начала теста из сессии
        start_time_str = request.session.get('start_time')
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
        else:
            start_time = timezone.now()

        end_time = timezone.now()
        test_duration = end_time - start_time

        # Преобразование test_duration в часы, минуты и секунды, удаление миллисекунд
        test_duration_str = str(timedelta(seconds=int(test_duration.total_seconds())))

        total_marks = 0
        correct_answers_count = 0
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
                    extended_question = ExtendedQuestion.objects.get(uid=question.uid)
                    correct_answers_objs = ExtendedAnswer.objects.filter(question_text=extended_question, is_correct=True)
                    correct_answers_text = [ans.text.strip().lower() for ans in correct_answers_objs]
                    if user_answers and any(user_answer.strip().lower() in correct_answers_text for user_answer in user_answers):
                        correct = True
                except ExtendedQuestion.DoesNotExist:
                    pass

            if correct:
                correct_answers_count += 1
                total_marks += question.marks
            else:
                incorrect_answers += 1

            results.append({
                'question': question.question,
                'user_answers': user_answers,
                'correct': correct
            })

        for question in extended_questions:
            user_answers = request.POST.getlist(str(question.uid))
            correct = False

            correct_answers_objs = ExtendedAnswer.objects.filter(question_text=question, is_correct=True)
            correct_answers_text = [ans.text.strip().lower() for ans in correct_answers_objs]
            if user_answers and any(user_answer.strip().lower() in correct_answers_text for user_answer in user_answers):
                correct = True

            if correct:
                correct_answers_count += 1
                total_marks += question.marks
            else:
                incorrect_answers += 1

            results.append({
                'question': question.text,
                'user_answers': user_answers,
                'correct': correct
            })

        context = {
            'total_marks': total_marks,
            'correct_answers': correct_answers_count,
            'incorrect_answers': incorrect_answers,
            'results': results,
            'test_duration': test_duration_str
        }
        return render(request, 'test/result.html', context)
    else:
        return redirect('home')
