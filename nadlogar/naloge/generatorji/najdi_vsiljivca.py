from .solski_slovar import SolskiSlovarGenerator
import random
from lxml import etree

class NajdiVsiljivca(SolskiSlovarGenerator):

    IME = 'Najdi vsiljivca'
    PREDLOGA = 'najdi_vsiljivca'
    NAVODILA = 'Poišči vsiljivca'
    
    def __init__(self):
        super().__init__()

class NajdiVsiljivcaSpol(NajdiVsiljivca):

    IME = 'Najdi vsiljivca glede na spol'
    NAVODILA = 'Poišči vsiljivca'
    
    def __init__(self):
        super().__init__()
    
    def generiraj_primere(self, n):
        spol_samostalnikov = {}

        # Najdemo vse samostalnike in jih glede na spol uredimo v slovar
        # spol_samostalnikov.
        samostalniki = self.slovar.xpath('//BV/samostalnik')
        for samostalnik in samostalniki:
            spol = samostalnik.text[0]
            geslo = samostalnik.getparent().getparent()
            iztocnica = geslo.xpath('iztočnica')[0].text

            if spol not in spol_samostalnikov:
                spol_samostalnikov[spol] = []
            spol_samostalnikov[spol].append(iztocnica)
        
        primeri = []

        while len(primeri) < n:
            # Izberemo dva nakljucna spola iz moznih spolov
            spol_vecina, spol_vsiljivec = random.sample(spol_samostalnikov.keys(), k=2)

            # Izberemo m besed spola spol_vecina in 1 besedo spola spol_vsiljivec
            vsiljivec = random.choice(spol_samostalnikov[spol_vsiljivec])
            ostali = random.sample(spol_samostalnikov[spol_vecina], k=3)

            izbor = ostali + [vsiljivec]
            random.shuffle(izbor)
            primeri.append({'besede': izbor, 'vsiljivec': vsiljivec})
        
        return primeri