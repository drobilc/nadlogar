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
    NAVODILA = 'Poišči vsiljivca glede na spol'
    
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

class NajdiVsiljivcaBesednaVrsta(NajdiVsiljivca):

    IME = 'Najdi vsiljivca glede na besedno vrsto'
    NAVODILA = 'Poišči vsiljivca glede na besedno vrsto'
    
    def __init__(self):
        super().__init__()
    
    def generiraj_primere(self, n):
        besedne_vrste_iztocnic = {}

        # Najdemo vse besede in jih glede na besedno vrst uredimo v slovar
        # besedne_vrste_iztocnic
        besedne_vrste = self.slovar.xpath('//BV')
        for besedna_vrsta in besedne_vrste:
            if len(besedna_vrsta) <= 0:
                continue

            geslo = besedna_vrsta.getparent()
            iztocnica_element = geslo.find('iztočnica')
            if iztocnica_element is None:
                continue
            iztocnica = iztocnica_element.text

            # Za besedno vrsto vzamemo kar ime xml oznake
            besedna_vrsta = besedna_vrsta[0].tag         

            if besedna_vrsta not in besedne_vrste_iztocnic:
                besedne_vrste_iztocnic[besedna_vrsta] = []
            besedne_vrste_iztocnic[besedna_vrsta].append(iztocnica)
        
        primeri = []

        while len(primeri) < n:
            # Izberemo dve nakljucni besedni vrsti iz vseh moznih besednih vrst
            besedna_vrsta_vecina, besedna_vrsta_vsiljivec = random.sample(besedne_vrste_iztocnic.keys(), k=2)

            # Izberemo m besed spola spol_vecina in 1 besedo spola spol_vsiljivec
            vsiljivec = random.choice(besedne_vrste_iztocnic[besedna_vrsta_vsiljivec])
            ostali = random.sample(besedne_vrste_iztocnic[besedna_vrsta_vecina], k=3)

            izbor = ostali + [vsiljivec]
            random.shuffle(izbor)
            primeri.append({'besede': izbor, 'vsiljivec': vsiljivec})
        
        return primeri