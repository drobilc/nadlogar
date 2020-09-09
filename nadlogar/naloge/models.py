from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import django.utils.timezone
from django.db.models import Max

from naloge.generatorji_nalog import *

# Vsi mozni tipi nalog, ki jih nasa storitev ponuja
GENERATORJI = [
    NalogaIzlociVsiljivcaSpol,
    NajdiVsiljivcaBesednaVrsta,
    NajdiVsiljivcaStevilo,
    NajdiVsiljivcaPredmetnoPodrocje,
    NalogaVstaviUstreznoObliko,
    NalogaDolociSlovnicnoStevilo,
    NalogaDolociSteviloPomenov,
    NalogaGlasVsiljivec
]

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
    
    def generator_nalog(self):
        # Glede na ime razreda generatorja poiscemo dejanski razred
        generator_razred = Naloga.GENERATOR_DICT[self.generator]
        # Ustvarimo nov objekt, ki pripada razredu, kot argumente mu podamo:
        #   * podatki - slovar s podatki s pomocjo katerega se zna objekt naloga
        #     nazaj sestaviti (obnoviti seznam primerov)
        #   * navodila - navodila naloge
        #   * stevilo_primerov - koliko primerov zelimo zgenerirati (nekatere
        #     naloge ta argument preprosto spregledajo in uporabnijo podatke iz
        #     slovarja podatki)
        return generator_razred(self.podatki, navodila=self.navodila, stevilo_primerov=self.stevilo_primerov)