from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.forms import ModelForm
from django.http import HttpResponse
from django.conf import settings
import uuid
import os

from .models import DelovniList, Naloga
from .generatorji.latex_generator import LatexGenerator
from .generatorji.obrazec_generator import ObrazecGenerator

def index(request):
    return render(request, 'landing_page.html')

@login_required
def seznam_dokumentov(request):
    # Ker ima uporabnik lahko vecje stevilo dokumentov je smiselno seznam
    # razdeliti na strani. Ce je v URL dodan GET parameter stran, potem
    # uporabniku prikazemo doloceno stran, sicer pa mu prikazemo kar prvo stran
    # z dokumenti.
    trenutna_stran = request.GET.get('stran', 1)

    # Dobimo seznam vseh dokumentov, ki pripadajo uporabniku, uredimo jih po
    # datumu zadnje spremembe.
    delovni_listi = DelovniList.objects.filter(lastnik=request.user).order_by('-updated_at')
    paginator = Paginator(delovni_listi, settings.STEVILO_DELOVNIH_LISTOV_NA_STRAN)

    # Pri pridobivanju dolocene strani lahko pride do napake, ce trenutna stran
    # ni stevilka ali ce je uporabnik presegel obseg svojih dokumentov. Ce
    # uporabnik posreduje neveljavno stran mu prikazemo kar prvo stran. Ce
    # uporabnik preseze stevilo strani, mu prikazemo kar zadnjo stran.
    try:
        seznam_delovnih_listov = paginator.page(trenutna_stran)
    except PageNotAnInteger:
        seznam_delovnih_listov = paginator.page(1)
    except EmptyPage:
        seznam_delovnih_listov = paginator.page(paginator.num_pages)
    except InvalidPage:
        seznam_delovnih_listov = paginator.page(1)

    return render(request, 'testi/seznam_dokumentov.html', {'delovni_listi': seznam_delovnih_listov})

@login_required
def podrobnosti_delovnega_lista(request, id_delovnega_lista: int):
    # Najprej poiscemo delovni list glede na prejet id. Ce uporabnik nima
    # pravice za ogled dokumenta vrnemo napako
    delovni_list: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)

    if not delovni_list.lahko_vidi(request.user):
        raise PermissionDenied

    return render(request, 'testi/podrobnosti_dokumenta.html', {'delovni_list': delovni_list})

@login_required
def odstranjevanje_delovnega_lista(request, id_delovnega_lista: int):
    # Najprej poiscemo delovni list glede na prejet id
    delovni_list: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)

    # Nato preverimo ali ima uporabnik sploh pravico do urejanja dokumenta. Ce
    # je nima, sprozimo Exception.
    if not delovni_list.lahko_ureja(request.user):
        raise PermissionDenied

    # Uporabniku sporocimo, da je bil delovni list uspesno izbrisan s pomocjo
    # django.messages knjiznice
    messages.add_message(request, messages.INFO, 'Delovni list "{}" je bil uspešno izbrisan.'.format(delovni_list.naslov))

    # Delovni list dejansko izbrisemo, vse povezane naloge se izbrisejo, ker je
    # brisanje kaskadno
    delovni_list.delete()

    # Uporabnika preusmerimo na seznam dokumentov, kjer se mu prikaze obvestilo,
    # da je bil delovni list izbrisan
    return redirect(reverse('naloge:seznam_dokumentov'))

@login_required
def ustvari_delovni_list(request):
    # Ustvarimo nov delovni list in uporabnika preusmerimo na stran za urejanje
    # tega delovnega lista
    nov_delovni_list = DelovniList.prazen_dokument(request.user)
    nov_delovni_list.save()
    return redirect(reverse('naloge:urejanje_delovnega_lista', kwargs={'id_delovnega_lista' : nov_delovni_list.id }))

class NalogaForm(ModelForm):
    class Meta:
        model = Naloga
        fields = ['generator', 'stevilo_primerov', 'navodila']

@login_required
def dodaj_nalogo(request, id_delovnega_lista: int):
    # Edina dovoljena metoda za dodajanje naloge je POST
    if request.method != 'POST':
        return HttpResponse(status=400)
    
    # Najprej poiscemo delovni list glede na prejet id
    delovni_list: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)
    
    # Preverimo ali ima uporabnik urejevalni dostop do delovnega lista.
    if not delovni_list.lahko_ureja(request.user):
        raise PermissionDenied
    
    # Glede na prejete POST podatke zapolnimo Naloga form. Ce je ta veljavna, ji
    # dodamo se delovni list in podatke shranimo.
    naloga_form: NalogaForm = NalogaForm(request.POST)
    if naloga_form.is_valid():
        naloga = naloga_form.save(commit=False)
        naloga.delovni_list = delovni_list
        naloga.save()
        return render(request, 'naloge/naloga.html', { 'naloga': naloga })
    
    return HttpResponse(status=400)

@login_required
def uredi_nalogo(request):

    if request.method != 'POST':
        return HttpResponse(status=400)

    # Pri posiljanju forme za urejanje naloge se na streznik posreduje id
    # naloge, ki jo zeli uporabnik urediti. Ce id naloge ni posredovan na
    # streznik vrnemo napako.
    naloga_id = request.POST.get('naloga_id', None)
    if naloga_id is None:
        return HttpResponse(status=400)

    # Preverimo ali obstaja naloga z iskanim id v bazi podatkov
    try:
        naloga = Naloga.objects.get(pk=naloga_id)
    except Exception:
        return HttpResponse(status=400)
    
    # Preverimo ali ima trenutno prijavljeni uporabnik sploh pravico urejati
    # nalogo. Ker je vsaka naloga le na ENEM delovnem listu, lahko preverimo ali
    # ima uporabnik sploh pravico urejati delovni list.
    if not naloga.delovni_list.lahko_ureja(request.user):
        raise PermissionDenied

    # Ko enkrat najdemo nalogo, iz requesta najdemo se akcijo, ki jo zeli
    # uporabnik izvesti. Ta je lahko ena izmed naslednjih moznosti:
    #   * odstrani_nalogo - izbrisi nalogo iz delovnega lista
    #   * premakni_gor - premakni nalogo eno mesto navzgor v delovnem listu
    #   * premakni_dol - premakni nalogo eno mesto navzdol v delovnem listu
    #   * ponovno_generiraj - ponovno generiraj primere naloge
    #   * dodaj_primer - dodaj en primer k nalogi
    #   * uredi_nalogo - sprejmi podatke obrazca za urejanje naloge, spremeni
    #     podatke naloge in ponovno generiraj nalogo
    action = request.POST.get('action', None)
    if action is None:
        return HttpResponse(status=400)

    # Glede na prejeto akcijo izvedi ustrezno dejanje in podatke shrani v bazo
    if action == 'odstrani_nalogo':
        naloga.delete()
    elif action == 'premakni_gor':
        naloga.premakni_gor()
    elif action == 'premakni_dol':
        naloga.premakni_dol()
    elif action == 'ponovno_generiraj':
        naloga.ponovno_generiraj()
        return render(request, 'naloge/naloga.html', { 'naloga': naloga })
    elif action == 'dodaj_primer':
        naloga.dodaj_primer()
        return render(request, 'naloge/naloga.html', { 'naloga': naloga })
    elif action == 'uredi_nalogo':
        obrazec = ObrazecGenerator.generiraj_obrazec(naloga, request)
        if obrazec.is_valid():
            naloga.posodobi_podatke(obrazec.cleaned_data)
            return render(request, 'naloge/naloga.html', { 'naloga': naloga })
        
    return HttpResponse(status=200)

class DelovniListForm(ModelForm):
    class Meta:
        model = DelovniList
        fields = ['naslov', 'opis']

@login_required
def urejanje_delovnega_lista(request, id_delovnega_lista: int):
    delovni_list: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)

    if not delovni_list.lahko_ureja(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        # Ce je uporabnik izpolnil formo za urejanje delovnega lista, posodobimo
        # podatke delovnega lista. Pri tem pa moramo paziti, da ne klicemo
        # neposredno delovni_list_form.save(), saj ima nas obrazec za urejanje
        # delovnega lista le dve polji - naslov in opis, namesto vseh zahtevanih
        # polj obrazca. Tako posodobimo le ustrezna polja v bazi.
        delovni_list_form: DelovniListForm = DelovniListForm(request.POST)
        if delovni_list_form.is_valid():
            delovni_list.naslov = delovni_list_form.cleaned_data['naslov']
            delovni_list.opis = delovni_list_form.cleaned_data['opis']
            delovni_list.save()
            return redirect(reverse('naloge:podrobnosti_delovnega_lista', kwargs={'id_delovnega_lista' : delovni_list.id }))
    
    # Ker zelimo uporabniku ob izbiri tipa naloge v spustnem seznamu ob
    # dodajanju naloge ponuditi privzeta navodila, sestavimo JSON objekt z
    # navodili vseh nalog, ki jih v dokumentu prikazemo z uporabo JavaScript.
    navodila = {}
    for generator, generator_razred in Naloga.GENERATOR_DICT.items():
        navodila[generator] = generator_razred.NAVODILA
    
    delovni_list_form: DelovniListForm = DelovniListForm(instance=delovni_list)
    naloga_form: NalogaForm = NalogaForm(initial={ 'stevilo_primerov': 4 })
    return render(request, 'testi/urejanje_dokumenta.html', {
        'delovni_list': delovni_list,
        'naloga_form': naloga_form,
        'delovni_list_form': delovni_list_form,
        'navodila': navodila
    })

@login_required
def generiraj_delovni_list(request, id_delovnega_lista: int):
    delovni_list: DelovniList = get_object_or_404(DelovniList, pk=id_delovnega_lista)

    if not delovni_list.lahko_vidi(request.user):
        raise PermissionDenied

    # Pri generiranju pdf dokumenta najprej ustvarimo "unikatno" (uuid4 sicer v
    # teoriji ni ravno unikaten, v praksi pa naceloma je) ime. To uporabimo za
    # shranjevanje pdf dokumentov na disk.
    random_name = uuid.uuid4()

    # Sestavimo pot do datoteke na disku kamor bomo shranili pdf dokument.
    ime_datoteke = os.path.join(settings.MEDIA_ROOT, str(random_name))

    # S pomocjo LaTeX generatorja zgeneriramo delovni list in ga shranimo
    dokument = LatexGenerator.generiraj_latex_dokument(delovni_list)
    dokument.generate_pdf(ime_datoteke, clean=True, clean_tex=True)

    # Uporabnika preusmerimo na URL za dostop do pdf dokumenta
    return redirect(settings.MEDIA_URL + str(random_name) + '.pdf')