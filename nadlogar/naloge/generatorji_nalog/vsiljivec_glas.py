from .generator_nalog import GeneratorNalog
from lxml import etree
import random

class NalogaGlasVsiljivec(GeneratorNalog):

    IME = 'Izloči vsiljivca - glas'
    NAVODILA = 'Kateri glas v vrstici je vsiljivec? Obkroži samoglasnik ali soglasnik.'

    PRIVZETA_BESEDA = 'glasovi'
    
    def __init__(self, *args, **kwargs):
        super(NalogaGlasVsiljivec, self).__init__(*args, **kwargs)
        self.beseda = self.podatki['beseda'] if 'beseda' in self.podatki else NalogaGlasVsiljivec.PRIVZETA_BESEDA

        # Odpremo solski slovar in si v objekt shranimo koren xml drevesa DOC
        with open('slovarji/solski_slovar.xml', 'r', encoding='utf-8') as slovar:
            self.slovar = etree.parse(slovar)
    
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