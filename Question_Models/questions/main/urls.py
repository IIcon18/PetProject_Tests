from django.urls import path
from .views import test_view, result_view

urlpatterns = [
    path('test/', test_view, name='test'),
    path('result/', result_view, name='result'),
]