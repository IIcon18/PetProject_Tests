from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='home'),
    path('account/', views.index, name='account'),
    path('account/manual', views.materials_home, name='manual')

]