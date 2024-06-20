from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='home'),
    path('account/', views.index, name='account'),
    path('account/materials/', views.materials_home, name='materials'),
    path('account/materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material-detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
