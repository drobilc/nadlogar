from django.conf import settings
from lxml import etree
import os

class GeneratorNalog(object):

    def __init__(self, naloga):
        # Vsak generator nalog vzdrzuje referenco na objekt v bazi podatkov in
        # slovar 'podatki', v katerem je shranjen seznam primerov in nastavitev
        # generatorja nalog.
        self.naloga = naloga

        # Za podatke vedno vzamemo slovar privzetih podatkov, ki mu nato dodamo
        # dodatne podatke, ki so morebiti ze shranjeni v bazi podatkov
        self.podatki = self.privzeti_podatki()
        if self.naloga.podatki is not None:
            self.podatki.update(self.naloga.podatki)
    
    def shrani(self):
        """Shrani spremenjene podatke v bazo podatkov"""
        self.naloga.podatki = self.podatki
        self.naloga.save()
    
    def privzeti_podatki(self):
        """Vrni slovar privzetih podatkov, ki se uporabijo, ce model Naloga v
        bazi podatkov se nima slovarja podatkov
        """
        return {}
    
    def podatki(self):
        """Vrni slovar podatkov naloge za shranjevanje v bazo podatkov"""
        return self.podatki
    
    def posodobi_podatke(self, novi_podatki):
        """Posodobi trenutne podatke generatorja in jih vrni"""   
        self.podatki.update(novi_podatki)
        return self.podatki
    
    def primeri(self):
        """Vrni seznam generiranih primerov naloge"""
        if 'primeri' not in self.podatki:
            self.generiraj_nalogo()
        return self.podatki['primeri'] 
    
    def generiraj_nalogo(self):
        """Ustvari seznam novih primerov naloge in jih vrni"""
        self.podatki['primeri'] = self.generiraj_primere(self.naloga.stevilo_primerov)
        return self.podatki
    
    def generiraj_primere(self, stevilo_primerov=6):
        """Ustvari seznam primerov in ga vrni"""
        novi_primeri = []
        while len(novi_primeri) < stevilo_primerov:
            novi_primeri.append(self.generiraj_primer())
        return novi_primeri

    def generiraj_primer(self):
        """Ustvari nov primer in vrni slovar tega primera"""
        return {}
    
    def accept(self, visitor, argument=None):
        """Sprejmi obiskovalca (Visitor pattern)"""
        return visitor.visit(self, argument)
    
    def dodaj_primer(self):
        """Dodaj nov primer na seznam primerov in vrni slovar podatkov"""
        novi_primeri = self.generiraj_primere(self.naloga.stevilo_primerov)
        self.podatki['primeri'].append(novi_primeri[0])
        return self.podatki['primeri']
    
    def odstrani_primer(self, indeks):
        if indeks < 0 or indeks > len(self.podatki['primeri']):
            return
        del self.podatki['primeri'][indeks]
        return self.podatki['primeri']

class GeneratorNalogSolskiSlovar(GeneratorNalog):
    """Posebna razlicica razreda GeneratorNalog, ki ima v spremenljivki slovar
    shranjen solski slovar
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Na pomnilnik preberemo celoten solski slovar, ki ga nato uporabljamo za
        # generiranje nalog
        ime_datoteke = os.path.join(settings.POT_DO_SLOVARJEV, 'solski_slovar.xml')
        with open(ime_datoteke, 'r', encoding='utf-8') as slovar:
            self.slovar = etree.parse(slovar)