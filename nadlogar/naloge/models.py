import random
from django.db import models

class Test(models.Model):
    naslov = models.CharField(max_length=255)
    datum = models.DateField()
    opis = models.TextField(blank=True)

    class Meta:
        ordering = ['datum', 'naslov']
        verbose_name_plural = 'testi'

    def __str__(self):
        return f'{self.naslov} ({self.datum})'

    def ustvari_nadlogo(self):
        primeri = []
        for naloga in self.naloge.all():
            primeri.append((naloga.ustvari_primer(), naloga))
        return primeri


class Naloga(models.Model):

    # Naloga predstavlja en tip naloge na dolocenem testu. Vsaka naloga zato
    # vsebuje naslednje podatke:
    #   * test - test na katerem se naloga nahaja
    #   * generator - ime generatorja, ki se uporablja za generiranje primerov
    #   * navodila - navodila naloge, ce niso podana, se kot privzeta vrednost
    #     vzame vrednost spremenljvike NAVODILA v generatorju
    #   * stevilo_primerov - stevilo primerov, ki jih naloga na testu vsebuje
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    generator = models.CharField(max_length=60)

    navodila = models.TextField(blank=True)
    stevilo_primerov = models.PositiveSmallIntegerField()

    class Meta:
        default_related_name = 'naloge'
        verbose_name_plural = 'naloge'
    
    def generiraj_primere(self, stevilo_primerov=6):
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        return {}

    def accept(self, visitor, argument=None):
        return visitor.visit(self, argument)