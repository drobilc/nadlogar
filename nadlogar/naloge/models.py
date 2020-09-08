from django.db import models
from django.conf import settings
import django.utils.timezone

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

class Test(models.Model):
    naslov = models.CharField(max_length=255)
    opis = models.TextField(blank=True)

    class Meta:
        ordering = ['naslov']
        verbose_name_plural = 'testi'

    def __str__(self):
        return f'{self.naslov}'
    
    @staticmethod
    def prazen_dokument():
        return Test(
            naslov=settings.PRAZEN_DOKUMENT['naslov'],
            opis=settings.PRAZEN_DOKUMENT['opis']
        )

class Naloga(models.Model):

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
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    generator = models.CharField(max_length=60, choices=GENERATOR)

    navodila = models.TextField(blank=True)
    stevilo_primerov = models.PositiveSmallIntegerField()
    podatki = models.JSONField(null=True, blank=True)

    class Meta:
        default_related_name = 'naloge'
        verbose_name_plural = 'naloge'
    
    def save(self, *args, **kwargs):
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
        return f'{self.test}: {self.get_generator_display()}, stevilo_primerov: {self.stevilo_primerov}'
    
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