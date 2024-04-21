from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_view, name='log'),
    path('', views.logout_view, name='home'),
]
