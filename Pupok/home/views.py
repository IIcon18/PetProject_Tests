from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import *
import random
from datetime import datetime, timedelta
from .models import TestResult

def home(request):
    return render(request, 'test/home.html')

def quiz(request):
    if request.method == 'POST':
        timer_expired = request.POST.get('timerExpired', 'false') == 'true'
        return render(request, 'result.html', {'timer_expired': timer_expired})
    else:
        num_questions = 25
        start_time = timezone.now()
        request.session['start_time'] = start_time.isoformat()

        all_questions = list(Question.objects.all())
        all_extended_questions = list(ExtendedQuestion.objects.all())

        for question in all_extended_questions:
            question.question_type = 'extended'

        combined_questions = all_questions + all_extended_questions
        random.shuffle(combined_questions)
        selected_questions = combined_questions[:num_questions]

        return render(request, 'test/quiz.html', {'questions': selected_questions})

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
        num_questions = 25  # Количество вопросов в тесте

        questions = list(Question.objects.all())
        extended_questions = list(ExtendedQuestion.objects.all())

        start_time_str = request.session.get('start_time')
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
        else:
            start_time = timezone.now()

        end_time = timezone.now()
        test_duration = end_time - start_time
        test_duration_str = str(timedelta(seconds=int(test_duration.total_seconds())))

        total_marks = 0
        correct_answers_count = 0
        incorrect_answers = 0
        results = []

        selected_question_ids = request.POST.getlist('selected_questions')

        for question in questions:
            if str(question.uid) in selected_question_ids:
                user_answers = request.POST.getlist(str(question.uid))
                correct = False

                if question.question_type == 'MCQ':
                    correct_answers = Answer.objects.filter(question=question, is_correct=True)
                    correct_answers_text = [ans.answer for ans in correct_answers]
                    if set(user_answers) == set(correct_answers_text):
                        correct = True
                else:
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
            if str(question.uid) in selected_question_ids:
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

        # Сохранение результата теста с указанием количества вопросов в тесте
        TestResult.objects.create(
            user=request.user,
            correct_answers=correct_answers_count,
            total_questions=num_questions,  # Используем заданное количество вопросов в тесте
            test_duration=test_duration
        )

        context = {
            'total_marks': total_marks,
            'correct_answers': correct_answers_count,
            'incorrect_answers': incorrect_answers,
            'results': results,
            'test_duration': test_duration_str
        }
        return render(request, 'test/result.html', context)
    else:
        return HttpResponseRedirect('/')

def results_list(request):
    results = TestResult.objects.all().order_by('-created_at')
    return render(request, 'test/result_list.html', {'results': results})
