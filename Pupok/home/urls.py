from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Ваши существующие URL-паттерны
    path('', views.home, name='home'),
    path('quiz/', views.quiz, name='quiz'),
    path('get-quiz/', views.get_quiz, name='get_quiz'),
    path('result/', views.result, name='result'),  # New route for result page
    path('account/results/', views.results_list, name='results_list'),  # URL для страницы результатов
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)