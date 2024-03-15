from .models import Article
from django.shortcuts import render
from django.http import HttpResponse
from .forms import loginform

def archive(request):
    posts = Article.objects.all()
    return render(request, 'archive.html', {"posts": posts})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise



def login(request):
    login=request.POST.get("logininput")
    passw=request.POST.get("passinput")
    print(login, passw)
    if login=="123" and passw=="123":
        return render(request, 'archive.html')
    else:
        return render(request, 'login.html')
    #submitbutton = request.POST.get("submit")
    #login = ""
    #passw = ""
    #form = loginform(request.POST)
    #if form.is_valid():
    #    passw = form.cleaned_data.get("name")
    #    login = form.cleaned_data.get("passw")
    #context = {
    #    'form': form, 'login':login, 'passw': passw, 'submitbutton': submitbutton
    #}

    #print( context["login"], context["passw"])
    #if context["login"] == "placeholderlogin" and context["passw"] == "placeholderpassw":
    #    return render(request, '')
    #else:
     #   return  render(request, 'login.html')

