from ..models import Naloga
from lxml import etree
import random

class NalogaDolociSteviloPomenov(Naloga):

    IME = 'Določi število pomenov - Franček'
    NAVODILA = 'Koliko pomenov imajo naslednje besede v slovarju Franček?'
    
    def __init__(self, navodila, stevilo_primerov=6):
        self.navodila = navodila
        self.stevilo_primerov = stevilo_primerov

        # Odpremo solski slovar in si v objekt shranimo koren xml drevesa DOC
        with open('slovarji/solski_slovar.xml', 'r', encoding='utf-8') as slovar:
            self.slovar = etree.parse(slovar)
        
        self.primeri = self.generiraj_primere(stevilo_primerov)
    
    def generiraj_primere(self, stevilo_primerov=6):
        self.stevila_pomenov = []

        gesla = self.slovar.xpath('//geslo')
        for geslo in gesla:
            iztocnica = geslo.xpath('iztočnica/text()')[0]
            stevilo_pomenov = int(geslo.xpath('count(pomen)'))
            self.stevila_pomenov.append((iztocnica, stevilo_pomenov))
        
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        izbor = random.choice(self.stevila_pomenov)
        return {'beseda': izbor[0], 'stevilo_pomenov': izbor[1]}