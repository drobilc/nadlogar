from .generator_nalog import GeneratorNalog
from lxml import etree
import random

class NalogaDolociSlovnicnoStevilo(GeneratorNalog):

    IME = 'Določevanje slovničnega števila'
    NAVODILA = 'Besedam določi slovnično število in jih vstavi v preglednico.'
    
    def __init__(self, *args, **kwargs):
        super(NalogaDolociSlovnicnoStevilo, self).__init__(*args, **kwargs)

        # Odpremo solski slovar in si v objekt shranimo koren xml drevesa DOC
        with open('slovarji/solski_slovar.xml', 'r', encoding='utf-8') as slovar:
            self.slovar = etree.parse(slovar)
    
    def generiraj_primere(self, stevilo_primerov=6):
        gesla = self.slovar.xpath('//geslo[oblike/dvojina/following-sibling::množina]')
        self.oblike = []
        for geslo in gesla:
            oblike = geslo.xpath('iztočnica/text() | oblike/dvojina/text() | oblike/množina/text()')
            if len(set(oblike)) < 3:
                continue
            self.oblike.append(oblike)
        
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self, stevilo_besed=12):
        izbor = random.sample(self.oblike, k=stevilo_besed)
        stevilcnost = [0, 1, 2] * ((stevilo_besed // 3) + 1)
        
        besede = []
        for i in range(stevilo_besed):
            besede.append(izbor[i][stevilcnost[i]])
        
        return {'besede': besede}