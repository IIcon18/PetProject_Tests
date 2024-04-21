from django.shortcuts import render
from .models import Questions

def tests_home(request):
    tests=Questions.objects.all()
    return render(request, 'main/tests.html', {"tests":tests})


