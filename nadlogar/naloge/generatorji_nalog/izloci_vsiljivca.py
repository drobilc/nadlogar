from .generator_nalog import GeneratorNalog
from lxml import etree
import random

class NalogaIzlociVsiljivca(GeneratorNalog):

    IME = 'Izloči vsiljivca'
    NAVODILA = 'Izloči vsiljivca'
    
    def __init__(self, *args, **kwargs):
        super(NalogaIzlociVsiljivca, self).__init__(*args, **kwargs)

        # Odpremo solski slovar in si v objekt shranimo koren xml drevesa DOC
        with open('slovarji/solski_slovar.xml', 'r', encoding='utf-8') as slovar:
            self.slovar = etree.parse(slovar)
    
    def sestavi_skupine(self):
        return {}

    def generiraj_primere(self, stevilo_primerov=6):
        skupine = self.sestavi_skupine()
        return [self.generiraj_primer(skupine) for i in range(stevilo_primerov)]
    
    def generiraj_primer(self, skupine):
        skupina_vecina, skupina_vsiljivec = random.sample(skupine.keys(), k=2)

        # Izberemo m besed spola skupina_vecina in 1 besedo spola skupina_vsiljivec
        vsiljivec = random.choice(skupine[skupina_vsiljivec])
        ostali = random.sample(skupine[skupina_vecina], k=3)

        izbor = ostali + [vsiljivec]
        random.shuffle(izbor)
        return {'besede': izbor, 'vsiljivec': vsiljivec}

class NalogaIzlociVsiljivcaSpol(NalogaIzlociVsiljivca):

    IME = 'Izloči vsiljivca - spol'
    NAVODILA = 'Izloči vsiljivca glede na spol.'

    def sestavi_skupine(self):
        spoli_samostalnikov = {}

        # Najdemo vse samostalnike in jih glede na spol uredimo v slovar
        # spol_samostalnikov.
        samostalniki = self.slovar.xpath('//BV/samostalnik')
        for samostalnik in samostalniki:
            spol = samostalnik.text[0]
            geslo = samostalnik.getparent().getparent()
            iztocnica = geslo.xpath('iztočnica')[0].text

            if spol not in spoli_samostalnikov:
                spoli_samostalnikov[spol] = []
            spoli_samostalnikov[spol].append(iztocnica)
        
        return spoli_samostalnikov

class NajdiVsiljivcaBesednaVrsta(NalogaIzlociVsiljivca):

    IME = 'Izloči vsiljivca - besedna vrsta'
    NAVODILA = 'Izloči vsiljivca glede na besedno vrsto.'

    def sestavi_skupine(self):
        besedne_vrste_iztocnic = {}

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
        
        return besedne_vrste_iztocnic

class NajdiVsiljivcaStevilo(NalogaIzlociVsiljivca):

    IME = 'Izloči vsiljivca - slovnično število'
    NAVODILA = 'Izloči vsiljivca glede na slovnično število.'

    def sestavi_skupine(self):
        stevila_iztocnic = {'ednina': [], 'dvojina': [], 'mnozina': []}

        gesla = self.slovar.xpath('//geslo[oblike/dvojina/following-sibling::množina]')
        for geslo in gesla:
            oblike = geslo.xpath('iztočnica/text() | oblike/dvojina/text() | oblike/množina/text()')
            if len(set(oblike)) < 3:
                continue

            stevila_iztocnic['ednina'].append(oblike[0])
            stevila_iztocnic['dvojina'].append(oblike[1])
            stevila_iztocnic['mnozina'].append(oblike[2])
        
        return stevila_iztocnic

class NajdiVsiljivcaPredmetnoPodrocje(NalogaIzlociVsiljivca):

    IME = 'Izloči vsiljivca - predmetno področje'
    NAVODILA = 'Izloči vsiljivca glede na področje.'

    def sestavi_skupine(self):
        podrocja_iztocnic = {}

        gesla = self.slovar.xpath('//geslo[pomen/področje]')
        for geslo in gesla:
            iztocnica = geslo.xpath('iztočnica/text()')[0]
            podrocja = geslo.xpath('pomen/področje/text()')
            filtrirana_podrocja = set(filter(lambda podrocja: 'problem' not in podrocja, podrocja))
            
            if len(filtrirana_podrocja) == 1:
                for podrocje in filtrirana_podrocja:
                    if podrocje not in podrocja_iztocnic:
                        podrocja_iztocnic[podrocje] = []
                    podrocja_iztocnic[podrocje].append(iztocnica)
        
        filtrirana_podrocja_iztocnic = {}
        for podrocje in podrocja_iztocnic:
            if len(podrocja_iztocnic[podrocje]) >= 3:
                filtrirana_podrocja_iztocnic[podrocje] = podrocja_iztocnic[podrocje]

        return filtrirana_podrocja_iztocnic