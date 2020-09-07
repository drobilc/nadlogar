from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.conf import settings
import uuid

from .models import Test, Naloga
from .generatorji.latex_generator import LatexGenerator

def index(request):
    return render(request, 'testi/landing_page.html')

def seznam_dokumentov(request):
    seznam_testov = Test.objects.all()
    return render(request, 'testi/seznam_testov.html', {'seznam_testov': seznam_testov})

def podrobnosti_delovnega_lista(request, id_delovnega_lista: int):
    test: Test = get_object_or_404(Test, pk=id_delovnega_lista)
    return render(request, 'testi/test.html', {'test': test, 'naloge': test.naloge.all()})

def urejanje_delovnega_lista(request, id_delovnega_lista: int):
    return HttpResponse('Urejanje delovnega lista {}'.format(id_delovnega_lista))

def generiraj_delovni_list(request, id_delovnega_lista: int):
    test: Test = get_object_or_404(Test, pk=id_delovnega_lista)

    random_name = uuid.uuid4()

    dokument = LatexGenerator.generate_latex(test)
    dokument.generate_pdf(settings.MEDIA_ROOT + str(random_name), clean=True, clean_tex=True)

    return redirect(settings.MEDIA_URL + str(random_name) + '.pdf')