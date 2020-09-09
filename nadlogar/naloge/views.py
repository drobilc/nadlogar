from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpResponse
from django.conf import settings
import uuid
import os

from .models import DelovniList, Naloga
from .generatorji.latex_generator import LatexGenerator
from .generatorji.html_generator import HtmlGenerator

def index(request):
    return render(request, 'landing_page.html')

@login_required
def seznam_dokumentov(request):
    delovni_listi = DelovniList.objects.filter(lastnik=request.user)
    return render(request, 'testi/seznam_dokumentov.html', {'delovni_listi': delovni_listi})

@login_required
def podrobnosti_delovnega_lista(request, id_delovnega_lista: int):
    test: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)
    return render(request, 'testi/podrobnosti_dokumenta.html', {'delovni_list': test, 'naloge': test.naloge.all()})

@login_required
def ustvari_delovni_list(request):
    nov_delovni_list = DelovniList.prazen_dokument(request.user)
    nov_delovni_list.save()
    return redirect(reverse('naloge:urejanje_delovnega_lista', kwargs={'id_delovnega_lista' : nov_delovni_list.id }))

class NalogaForm(ModelForm):
    class Meta:
        model = Naloga
        fields = ['generator', 'stevilo_primerov', 'navodila']

@login_required
def dodaj_nalogo(request, id_delovnega_lista: int):
    delovni_list: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)
    
    if request.method == 'POST':
        naloga_form: NalogaForm = NalogaForm(request.POST)
        if naloga_form.is_valid():
            naloga = naloga_form.save(commit=False)
            naloga.delovni_list = delovni_list
            naloga.save()

            try:
                html = HtmlGenerator.generiraj_html(naloga.generator_nalog())
                return HttpResponse(html)
            except Exception:
                return HttpResponse(status=400)
    
    return HttpResponse(status=400)

@login_required
def odstrani_nalogo(request, id_delovnega_lista: int):
    delovni_list: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)

    if request.method == 'POST':
        naloga_id = request.POST.get('naloga_id', None)
        if naloga_id is not None:
            try:
                naloga = Naloga.objects.get(pk=naloga_id)
                naloga.delete()
                return HttpResponse(status=200)
            except Exception:
                return HttpResponse(status=400)

    return HttpResponse(status=400)

class DelovniListForm(ModelForm):
    class Meta:
        model = DelovniList
        fields = ['naslov', 'opis']

@login_required
def urejanje_delovnega_lista(request, id_delovnega_lista: int):
    test: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)

    if request.method == 'POST':
        delovni_list_form: DelovniListForm = DelovniListForm(request.POST)
        if delovni_list_form.is_valid():
            test.naslov = delovni_list_form.cleaned_data['naslov']
            test.opis = delovni_list_form.cleaned_data['opis']
            test.save()
            return redirect(reverse('naloge:podrobnosti_delovnega_lista', kwargs={'id_delovnega_lista' : test.id }))
    
    delovni_list_form: DelovniListForm = DelovniListForm(instance=test)
    naloga_form: NalogaForm = NalogaForm(initial={
        'stevilo_primerov': 4
    })
    return render(request, 'testi/urejanje_dokumenta.html', {
        'delovni_list': test,
        'naloge': test.naloge.all(),
        'naloga_form': naloga_form,
        'delovni_list_form': delovni_list_form
    })

@login_required
def generiraj_delovni_list(request, id_delovnega_lista: int):
    test: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)

    random_name = uuid.uuid4()

    dokument = LatexGenerator.generate_latex(test)
    ime_datoteke = os.path.join(settings.MEDIA_ROOT, str(random_name))
    dokument.generate_pdf(ime_datoteke, clean=True, clean_tex=True)

    return redirect(settings.MEDIA_URL + str(random_name) + '.pdf')