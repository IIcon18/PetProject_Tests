from django.shortcuts import render,  redirect
from django.http import JsonResponse  
from django.http import HttpResponse  

from .models import *

import random

def home(request):
    context = {'catgories': Types.objects.all()}
    
    if request.GET.get('gfg'):
        return redirect(f"quiz/?gfg={request.GET.get('gfg')}")
    
    return render(request, 'test/home.html', context)

def quiz(request):
    context = {'gfg': request.GET.get('gfg')}
    print(request.GET.get('gfg'))
    return render(request, 'test/quiz.html', context)



def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        
        if request.GET.get('gfg'):
            question_objs = question_objs.filter(gfg__gfg_name__icontains = request.GET.get('gfg'))
            
        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)
        
        
        for question_obj in question_objs:
            
            data.append({
                "uid" : question_obj.uid,
                "gfg": question_obj.gfg.gfg_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answer" : question_obj.get_answers(),
            })

        payload = {'status': True, 'data': data}
        
        return JsonResponse(payload)  # Return JsonResponse
        
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")
