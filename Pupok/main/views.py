from django.views.generic import DetailView
from django.shortcuts import render
from .models import Document

def materials_home(request):
    documents = Document.objects.all()
    return render(request, 'main/materials.html', {'documents': documents})

class MaterialDetailView(DetailView):
    model = Document
    template_name = 'material_detail.html'

def login(request):
    return render(request, 'main/login.html')

def index(request):
    return render(request, 'main/index.html')

def manual(request):
    return render(request, 'main/manual.html')

def home(request):
    return render(request, 'test/home.html')

def quiz(request):
    return render(request, 'test/quiz.html')

def get_quiz(request):
    return render(request, 'test/quiz.html')

def result(request):
    return render(request, 'test/result.html')