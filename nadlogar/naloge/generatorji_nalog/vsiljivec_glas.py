from ..models import Naloga
from lxml import etree
import random

class NalogaGlasVsiljivec(Naloga):

    IME = 'Izloči vsiljivca - glas'
    NAVODILA = 'Kateri glas v vrstici je vsiljivec? Obkroži samoglasnik ali soglasnik.'
    
    def __init__(self, navodila, beseda, stevilo_primerov=6):
        self.navodila = navodila
        self.beseda = beseda

        # Odpremo solski slovar in si v objekt shranimo koren xml drevesa DOC
        with open('slovarji/solski_slovar.xml', 'r', encoding='utf-8') as slovar:
            self.slovar = etree.parse(slovar)

        self.primeri = self.generiraj_primere(beseda)
    
    def generiraj_primere(self, beseda):        
        return [self.generiraj_primer(glas) for glas in beseda]
    
    def generiraj_primer(self, glas):
        samoglasniki, soglasniki = [c for c in 'aeiou'], [c for c in 'bcčdfghjklmnprsštvzž']
        glasovi = [glas]
        if glas in samoglasniki:
            glasovi.extend(random.sample(soglasniki, k=4))
        else:
            glasovi.extend(random.sample(samoglasniki, k=4))
        
        random.shuffle(glasovi)

        return {'glasovi': glasovi}