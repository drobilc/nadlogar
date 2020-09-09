from .generator_nalog import GeneratorNalog
from django.conf import settings
from lxml import etree
import random

class NalogaDolociSteviloPomenov(GeneratorNalog):

    IME = 'Določi število pomenov - Franček'
    NAVODILA = 'Koliko pomenov imajo naslednje besede v slovarju Franček?'
    
    def __init__(self, *args, **kwargs):
        super(NalogaDolociSteviloPomenov, self).__init__(*args, **kwargs)
        self.slovar = settings.SOLSKI_SLOVAR
    
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