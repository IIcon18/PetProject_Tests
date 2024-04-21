from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
def login_view(request):
       if request.method == 'POST':
           username = request.POST['username']
           password = request.POST['password']
           user = authenticate(request, username=username, password=password)
           if user is not None:
               login(request, user)
               return redirect('/account')  # Замените 'home' на URL вашей главной страницы
           else:
               messages.error(request, 'Invalid username or password.')
       return render(request, 'main/login.html')
def logout_view(request):
       logout(request)
       return redirect('/login')