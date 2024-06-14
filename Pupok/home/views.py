def result(request):
    try:
        if request.method == 'POST':
            print("Received POST request")
            questions = Question.objects.all()
            if request.GET.get('gfg'):
                questions = questions.filter(gfg__gfg_name__icontains=request.GET.get('gfg'))
            
            total_marks = 0
            correct_answers = 0
            incorrect_answers = 0
            results = []

            for question in questions:
                user_answer = request.POST.get(str(question.uid))
                print(f"Question: {question.question}, User Answer: {user_answer}")
                correct = False

                if question.question_type == 'MCQ':
                    correct_answer = Answer.objects.filter(question=question, is_correct=True).first()
                    print(f"Correct Answer: {correct_answer.answer if correct_answer else 'None'}")
                    if correct_answer and user_answer == correct_answer.answer:
                        correct = True
                else:  # SA type
                    try:
                        extended_question = ExtendedQuestion.objects.get(pk=question.uid)
                        correct_answers_objs = ExtendedAnswer.objects.filter(question=extended_question)
                        for ans in correct_answers_objs:
                            print(f"Extended Answer: {ans.text}")
                            if user_answer and user_answer.strip().lower() == ans.text.strip().lower():
                                correct = True
                                break
                    except ExtendedQuestion.DoesNotExist:
                        print(f"ExtendedQuestion with UID {question.uid} does not exist.")

                if correct:
                    correct_answers += 1
                    total_marks += question.marks
                else:
                    incorrect_answers += 1

                results.append({
                    'question': question.question,
                    'user_answer': user_answer,
                    'correct': correct
                })

            context = {
                'total_marks': total_marks,
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'results': results,
            }
            return render(request, 'test/result.html', context)
        else:
            return redirect('home')
    except Exception as e:
        print(f"Exception: {e}")
        return HttpResponse("Something went wrong")
