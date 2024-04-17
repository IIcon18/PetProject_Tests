from django.shortcuts import render
from .models import Articles

def materials_home(request):
    materials = Articles.objects.all()
    return render(request, 'main/manual.html',{'materials':materials})


def login(request):
    return render(request, 'main/login.html')

def index(request):
    return render(request, 'main/index.html')


def manual(request):
    return render(request, 'main/manual.html')