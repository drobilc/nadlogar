from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'naloge'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.podrobnosti, name='test_podrobnosti'),
    path('<int:pk>/pdf', views.test_pdf, name='test_generiraj_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)