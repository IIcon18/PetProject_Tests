from django.shortcuts import render
def tests_home(request):
    return render(request, 'main/tests.html')
