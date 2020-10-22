from .generator_nalog import GeneratorNalogSolskiSlovar
from lxml import etree
import random

class NalogaGlasVsiljivec(GeneratorNalogSolskiSlovar):

    IME = 'Izloči vsiljivca - glas'
    NAVODILA = 'Med navedenimi glasovi (samoglasniki in soglasniki) v vsaki vrstici obkroži tisti glas, ki je drugačne vrste.'
    
    def privzeti_podatki(self):
        return { 'beseda': 'glasovi' }
    
    def generiraj_nalogo(self):
        self.podatki['primeri'] = self.generiraj_primere(self.podatki['beseda'])
        return self.podatki
    
    def generiraj_primere(self, beseda):
        return [self.generiraj_primer(glas) for glas in beseda]
    
    def generiraj_primer(self, glas):
        glas = glas.lower()
        samoglasniki, soglasniki = 'aeiou', 'bcčdfghjklmnprsštvzž'
        glasovi = [glas]
        if glas in samoglasniki:
            glasovi.extend(random.sample(soglasniki, k=4))
        else:
            glasovi.extend(random.sample(samoglasniki, k=4))
        
        random.shuffle(glasovi)

        return { 'glasovi': glasovi }