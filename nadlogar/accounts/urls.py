from django.contrib.auth import views as authentication_views
from accounts import views
from django.urls import path

app_name = 'racuni'

urlpatterns = [
    path('prijava/', authentication_views.LoginView.as_view(template_name="registration/login.html"), name='prijava'),
    path('odjava/', authentication_views.LogoutView.as_view(), name='odjava'),
    path('vpis/', views.registracija, name='registracija'),
    path('novogeslo/', views.pozabljeno_geslo, name='pozabljeno_geslo'),
]