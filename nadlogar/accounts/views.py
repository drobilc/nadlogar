from django.shortcuts import redirect
from django.conf import settings

def registracija(request):
    return redirect(settings.FRANCEK_REGISTRACIJA)

def pozabljeno_geslo(request):
    return redirect(settings.FRANCEK_POZABLJENO_GESLO)