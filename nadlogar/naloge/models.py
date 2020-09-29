from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import django.utils.timezone
from django.db.models import Max, Min

from naloge.generatorji_nalog import *

# V prihodnosti bo morda potrebno dodati kaksne podatke uporabnikom, zato je
# smiselno, da ze vnaprej pripravimo model za uporabnika, saj je sicer z
# ustvarjanjem baze potrebno dosti vec dela
class Uporabnik(AbstractUser):
    pass

# Ker bomo za vec objektov najverjetneje belezili cas ustvarjanja in zadnjo
# posodobitev, ustvarimo nov abstrakten objekt TImeStapMixin
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class DelovniList(TimeStampMixin):
    naslov = models.CharField(max_length=255)
    opis = models.TextField(blank=True)
    lastnik = models.ForeignKey(Uporabnik, on_delete=models.CASCADE)

    class Meta:
        ordering = ['naslov']
        verbose_name_plural = 'delovni listi'

    def __str__(self):
        return f'{self.naslov}'
    
    def lahko_vidi(self, uporabnik):
        return uporabnik == self.lastnik
    
    def lahko_ureja(self, uporabnik):
        return uporabnik == self.lastnik
    
    @staticmethod
    def prazen_dokument(lastnik):
        return DelovniList(
            naslov=settings.PRAZEN_DOKUMENT['naslov'],
            opis=settings.PRAZEN_DOKUMENT['opis'],
            lastnik=lastnik
        )

class Naloga(TimeStampMixin):

    # Generatorji nalog se nahajajo v naloge.generatorji. V bazo zapisemo ime
    # razreda generatorja, uporabniku pa prikazemo ime, ki je zapisano v
    # staticni spremenljivki IME v generatorju.
    GENERATOR = [(generator.__name__, generator.IME) for generator in GENERATORJI]

    # Slovar, ki preslika ime generatorja v razred generatorja
    GENERATOR_DICT = dict([(generator.__name__, generator) for generator in GENERATORJI])

    # Naloga predstavlja en tip naloge na dolocenem testu. Vsaka naloga zato
    # vsebuje naslednje podatke:
    #   * test - test na katerem se naloga nahaja
    #   * generator - ime generatorja, ki se uporablja za generiranje primerov
    #   * navodila - navodila naloge, ce niso podana, se kot privzeta vrednost
    #     vzame vrednost spremenljvike NAVODILA v generatorju
    #   * stevilo_primerov - stevilo primerov, ki jih naloga na testu vsebuje
    delovni_list = models.ForeignKey(DelovniList, on_delete=models.CASCADE)
    generator = models.CharField(max_length=60, choices=GENERATOR)

    navodila = models.TextField(blank=True)
    stevilo_primerov = models.PositiveSmallIntegerField()
    podatki = models.JSONField(null=True, blank=True)

    # Na katerem mestu v dokumentu je ta naloga - manjsa stevilka pomeni, da je
    # naloga visje v dokumentu
    polozaj_v_dokumentu = models.IntegerField()

    class Meta:
        ordering = ['polozaj_v_dokumentu']
        default_related_name = 'naloge'
        verbose_name_plural = 'naloge'
    
    def save(self, *args, **kwargs):
        # Ce naloga se nima nastavljenega polozaja v dokumentu najprej najdemo
        # vse naloge v delovnem listu in za polozaj izberemo najvecji polozaj
        # ostalih nalog
        if self.polozaj_v_dokumentu is None:
            if self.delovni_list.naloge.count() <= 0:
                # Prva naloga naj ima polozaj = 1
                self.polozaj_v_dokumentu = 1
            else:
                najvecji_polozaj = self.delovni_list.naloge.all().aggregate(polozaj=Max('polozaj_v_dokumentu'))
                self.polozaj_v_dokumentu = najvecji_polozaj['polozaj'] + 1

        # Ce navodila naloge niso podana, jih pred shranjevanjem preberemo iz
        # generatorja
        if self.navodila is None or len(self.navodila) <= 0:
            generator_razred = Naloga.GENERATOR_DICT[self.generator]
            self.navodila = generator_razred.NAVODILA
        
        # Pred shranjevanjem naloge v bazo podatkov, preverimo ali podatki
        # naloge se niso bili zgenerirani (t.j. v primeru, da ima self.podatki
        # vrednost None)
        if self.podatki is None:
            generator_nalog = self.generator_nalog()
            self.podatki = generator_nalog.generiraj_nalogo()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.delovni_list}: {self.get_generator_display()}, stevilo_primerov: {self.stevilo_primerov}'
    
    def generator_nalog_razred(self):
        return Naloga.GENERATOR_DICT[self.generator]

    def generator_nalog(self):
        generator_razred = Naloga.GENERATOR_DICT[self.generator]
        return generator_razred(self)
    
    def primeri(self):
        return self.generator_nalog().primeri()
    
    def posodobi_podatke(self, podatki):
        # Seznam polj, ki jih je dovoljeno spremeniti 
        posodobi_polja = ['navodila', 'stevilo_primerov']

        # Spremenimo seznam dovoljenih polj
        for polje in posodobi_polja:
            if polje in podatki:
                setattr(self, polje, podatki[polje])
                # Odstrani polje iz seznama podatkov, da jih ne shranjujemo v
                # slovar podatkov naloge po nepotrebnem
                del podatki[polje]
        
        # Katerih polj ne shranjujemo v slovar podatkov naloge
        nedovoljena_polja = ['naloga_id', 'action']
        for polje in nedovoljena_polja:
            if polje in podatki:
                del podatki[polje]
        
        # Ko so podatki v modelu naloga spremenjeni, zahtevaj od generatorja
        # nalog posodobitev podatkov, nato znova generiraj nalogo in podatke
        # shrani v bazo podatkov
        generator_nalog = self.generator_nalog()
        generator_nalog.posodobi_podatke(podatki)
        generator_nalog.generiraj_nalogo()
        generator_nalog.shrani()
    
    def ponovno_generiraj(self):
        generator_nalog = self.generator_nalog()
        generator_nalog.generiraj_nalogo()
        generator_nalog.shrani()
    
    def dodaj_primer(self):
        self.stevilo_primerov += 1
        generator_nalog = self.generator_nalog()
        generator_nalog.dodaj_primer()
        generator_nalog.shrani()
    
    def odstrani_primer(self, indeks):
        self.stevilo_primerov -= 1
        generator_nalog = self.generator_nalog()
        generator_nalog.odstrani_primer(indeks)
        generator_nalog.shrani()
    
    def premakni_gor(self):
        prejsnje_naloge = self.delovni_list.naloge.filter(polozaj_v_dokumentu__lt=self.polozaj_v_dokumentu).order_by('-polozaj_v_dokumentu')
        # Ce je ta naloga prva na seznamu, potem ni kaj premikati
        if prejsnje_naloge.count() <= 0:
            return
        
        prejsnja_naloga = prejsnje_naloge[0]
        trenutni_polozaj = self.polozaj_v_dokumentu
        self.polozaj_v_dokumentu = prejsnja_naloga.polozaj_v_dokumentu
        prejsnja_naloga.polozaj_v_dokumentu = trenutni_polozaj

        self.save()
        prejsnja_naloga.save()

    def premakni_dol(self):
        naslednje_naloge = self.delovni_list.naloge.filter(polozaj_v_dokumentu__gt=self.polozaj_v_dokumentu).order_by('polozaj_v_dokumentu')
        # Ce je ta naloga zadnja na seznamu, potem ni kaj premikati
        if naslednje_naloge.count() <= 0:
            return
        
        naslednja_naloga = naslednje_naloge[0]
        trenutni_polozaj = self.polozaj_v_dokumentu
        self.polozaj_v_dokumentu = naslednja_naloga.polozaj_v_dokumentu
        naslednja_naloga.polozaj_v_dokumentu = trenutni_polozaj

        self.save()
        naslednja_naloga.save()