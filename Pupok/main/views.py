from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'main/login.html')

def index(request):
    return render(request, 'main/index.html')


def manual(request):
    return render(request, 'main/manual.html')