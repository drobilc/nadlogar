from django.urls import path

from . import views

app_name = 'naloge'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.podrobnosti, name='test_podrobnosti'),
]