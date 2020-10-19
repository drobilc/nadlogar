from .generator_nalog import GeneratorNalogSolskiSlovar
from lxml import etree
import random

class NalogaDolociSteviloPomenov(GeneratorNalogSolskiSlovar):

    IME = 'Določi število pomenov - Franček'
    NAVODILA = 'Navedene besede preveri v Šolskem slovarju slovenskega jezika na portalu Franček in ugotovi, koliko pomenov imajo. Obkroži pravilen odgovor.'
    
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