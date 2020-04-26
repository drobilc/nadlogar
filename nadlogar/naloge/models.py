import random
from django.db import models

# Vkljucevanje generatorjev nalog iz modula generatorji
from naloge.generatorji.vstavi_ustrezno_obliko import VstaviUstreznoOblikoGenerator
from naloge.generatorji.najdi_vsiljivca import *

# Seznam razredov vseh generatorjev, ki so uporabniku na voljo
GENERATORJI = [
    VstaviUstreznoOblikoGenerator,
    NajdiVsiljivcaSpol
]

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
    test = models.ForeignKey('testi.Test', on_delete=models.CASCADE)
    generator = models.CharField(max_length=60, choices=GENERATOR)

    navodila = models.TextField(blank=True)
    stevilo_primerov = models.PositiveSmallIntegerField()

    class Meta:
        default_related_name = 'naloge'
        verbose_name_plural = 'naloge'
    
    def save(self, *args, **kwargs):
        # Ce navodila naloge niso podana, jih pred shranjevanjem preberemo iz
        # generatorja
        if self.navodila is None or len(self.navodila) <= 0:
            generator = self.GENERATOR_DICT[self.generator]
            self.navodila = generator.NAVODILA
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.test}: {self.get_generator_display()}, stevilo_primerov: {self.stevilo_primerov}'

    def generiraj(self):
        # Glede na tip generatorja nalog, generiramo self.stevilo_primerov
        # primerov naloge
        generator = self.GENERATOR_DICT[self.generator]()
        return generator.generiraj_primere(self.stevilo_primerov)

    def ime_predloge(self):
        # Glede na ime generatorja, najprej poiscemo razred v slovarju
        # GENERATOR_DICT in iz razreda poberemo staticno spremenljivko PREDLOGA
        generator = self.GENERATOR_DICT[self.generator]
        return 'naloge/{ime_predloge}.html'.format(ime_predloge=generator.PREDLOGA)
