from django.shortcuts import render
from .models import Articles
from django.views.generic import DetailView

def materials_home(request):
    materials = Articles.objects.all()
    return render(request, 'main/manual.html',{'materials':materials})


def login(request):
    return render(request, 'main/login.html')

def index(request):
    return render(request, 'main/index.html')


def manual(request):
    return render(request, 'main/manual.html')

class NewsDetailView(DetailView):
    model = Articles
    template_name ='main/details_view.html'
    context_object_name = 'article'