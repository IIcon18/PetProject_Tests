from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import *
import random
from datetime import datetime, timedelta

def home(request):
    return render(request, 'test/home.html')

def quiz(request):
    if request.method == 'POST':
        timer_expired = request.POST.get('timerExpired', 'false') == 'true'
        return render(request, 'result.html', {'timer_expired': timer_expired})
    else:
        num_questions = 30
        num_hard = 8
        num_medium = (num_questions - num_hard) // 2
        num_easy = num_questions - num_hard - num_medium

        block_size = 10  # Размер блока можно изменить по необходимости

        start_time = timezone.now()
        request.session['start_time'] = start_time.isoformat()

        easy_questions = list(Question.objects.filter(difficulty='easy'))
        medium_questions = list(Question.objects.filter(difficulty='medium'))
        hard_questions = list(Question.objects.filter(difficulty='hard'))

        easy_extended_questions = list(ExtendedQuestion.objects.filter(difficulty='easy'))
        medium_extended_questions = list(ExtendedQuestion.objects.filter(difficulty='medium'))
        hard_extended_questions = list(ExtendedQuestion.objects.filter(difficulty='hard'))

        for question in easy_extended_questions + medium_extended_questions + hard_extended_questions:
            question.question_type = 'extended'

        combined_easy_questions = easy_questions + easy_extended_questions
        combined_medium_questions = medium_questions + medium_extended_questions
        combined_hard_questions = hard_questions + hard_extended_questions

        random.shuffle(combined_easy_questions)
        random.shuffle(combined_medium_questions)
        random.shuffle(combined_hard_questions)

        selected_easy_questions = combined_easy_questions[:num_easy]
        selected_medium_questions = combined_medium_questions[:num_medium]
        selected_hard_questions = combined_hard_questions[:num_hard]

        selected_questions = selected_easy_questions + selected_medium_questions + selected_hard_questions
        random.shuffle(selected_questions)

        # Разбиваем вопросы на блоки
        question_blocks = []
        current_block = []
        for index, question in enumerate(selected_questions, start=1):
            current_block.append(question)
            if len(current_block) == block_size:
                block_label = chr(65 + len(question_blocks))  # Генерация метки блока (A, B, C, ...)
                question_blocks.append((block_label, current_block))
                current_block = []
        
        if current_block:
            block_label = chr(65 + len(question_blocks))
            question_blocks.append((block_label, current_block))

        return render(request, 'test/quiz.html', {'question_blocks': question_blocks})

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

        num_questions = 30  # количество вопросов в тесте

        # Найти и обновить существующую запись результата теста, если она существует
        test_result, created = TestResult.objects.update_or_create(
            user=request.user,
            defaults={
                'correct_answers': correct_answers_count,
                'total_questions': num_questions,
                'test_duration': test_duration,
                'created_at': end_time  # Обновление времени прохождения теста
            }
        )

        return render(request, 'test/result.html', {
            'total_marks': total_marks,
            'correct_answers': correct_answers_count,
            'incorrect_answers': incorrect_answers,
            'test_duration': test_duration_str,
            'results': results
        })

    else:
        return HttpResponseRedirect('/')

def results_list(request):
    results = TestResult.objects.all().order_by('-created_at')
    return render(request, 'test/result_list.html', {'results': results})