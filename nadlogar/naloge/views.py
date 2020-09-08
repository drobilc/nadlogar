from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponse
from django.conf import settings
import uuid

from .models import Test, Naloga
from .generatorji.latex_generator import LatexGenerator

def index(request):
    return render(request, 'landing_page.html')

def seznam_dokumentov(request):
    delovni_listi = Test.objects.all()
    return render(request, 'testi/seznam_dokumentov.html', {'delovni_listi': delovni_listi})

def podrobnosti_delovnega_lista(request, id_delovnega_lista: int):
    test: Test = get_object_or_404(Test, pk=id_delovnega_lista)
    return render(request, 'testi/podrobnosti_dokumenta.html', {'delovni_list': test, 'naloge': test.naloge.all()})

def ustvari_delovni_list(request):
    nov_delovni_list = Test.prazen_dokument()
    nov_delovni_list.save()
    return redirect(reverse('naloge:urejanje_delovnega_lista', kwargs={'id_delovnega_lista' : nov_delovni_list.id }))

def urejanje_delovnega_lista(request, id_delovnega_lista: int):
    test: Test = get_object_or_404(Test, pk=id_delovnega_lista)
    return render(request, 'testi/urejanje_dokumenta.html', {'delovni_list': test, 'naloge': test.naloge.all()})

def generiraj_delovni_list(request, id_delovnega_lista: int):
    test: Test = get_object_or_404(Test, pk=id_delovnega_lista)

    random_name = uuid.uuid4()

    dokument = LatexGenerator.generate_latex(test)
    dokument.generate_pdf(settings.MEDIA_ROOT + str(random_name), clean=True, clean_tex=True)

    return redirect(settings.MEDIA_URL + str(random_name) + '.pdf')