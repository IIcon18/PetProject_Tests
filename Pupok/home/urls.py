from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz, name='quiz'),
    path('get-quiz/', views.get_quiz, name='get_quiz'),
    path('result/', views.result, name='result'),  # New route for result page
]
