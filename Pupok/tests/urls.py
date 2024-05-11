from django.urls import path
from . import views

urlpatterns = [
    path('', views.tests_home, name='home'),

]