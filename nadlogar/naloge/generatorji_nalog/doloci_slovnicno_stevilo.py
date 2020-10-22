from .generator_nalog import GeneratorNalogSolskiSlovar
from lxml import etree
import random

class NalogaRazvrstiVPreglednico(GeneratorNalogSolskiSlovar):

    IME = 'Razvrsti v preglednico'
    NAVODILA = 'Navedene besede zapiši v ustrezno polje v preglednici.'

    def sestavi_skupine(self):
        return {}

    def generiraj_primere(self, stevilo_primerov=6):
        skupine = self.sestavi_skupine()
        return [self.generiraj_primer(skupine) for i in range(stevilo_primerov)]
    
    def generiraj_primer(self, skupine, stevilo_iztocnic=12):
        # Iz vsake skupine izberemo stevilo_iztocnic / stevilo_skupin besed
        imena_skupin = list(skupine.keys())
        stevilo_skupin = len(imena_skupin)

        izbrane_iztocnice = []

        for i in range(stevilo_iztocnic):
            trenutna_skupina = imena_skupin[i % stevilo_skupin]

            ponovno_izberi = True
            while ponovno_izberi:
                izbrana_iztocnica = random.choice(skupine[trenutna_skupina])
                ponovno_izberi = izbrana_iztocnica in izbrane_iztocnice
            
            izbrane_iztocnice.append(izbrana_iztocnica)
        
        # Nakljucno pomesaj seznam besed
        random.shuffle(izbrane_iztocnice)
        
        return {'besede': izbrane_iztocnice, 'skupine': imena_skupin}

class NalogaRazvrstiVPreglednicoStevilo(NalogaRazvrstiVPreglednico):

    IME = 'Določevanje slovničnega števila'
    NAVODILA = 'Navedenim besedam določi slovnično število in jih zapiši v ustrezno polje v preglednici.'
    
    def sestavi_skupine(self):

        skupine = { 'Ednina': [], 'Dvojina': [], 'Množina': [] }

        gesla = self.slovar.xpath('//geslo[oblike/dvojina/following-sibling::množina]')
        for geslo in gesla:
            oblike = geslo.xpath('iztočnica/text() | oblike/dvojina/text() | oblike/množina/text()')
            if len(set(oblike)) < 3:
                continue
            skupine['Ednina'].append(oblike[0])
            skupine['Dvojina'].append(oblike[1])
            skupine['Množina'].append(oblike[2])
        
        return skupine

class NalogaRazvrstiVPreglednicoSpol(NalogaRazvrstiVPreglednico):

    IME = 'Razvrsti v preglednico glede na spol'
    NAVODILA = 'Navedenim samostalnikom določi spol in jih zapiši v ustrezno polje v preglednici.'
    
    def sestavi_skupine(self):

        skupine = { 'Moški spol': [], 'Ženski spol': [], 'Srednji spol': [] }
        ime_skupine = {
            'm': 'Moški spol', 'm mn.': 'Moški spol',
            'ž': 'Ženski spol', 'ž mn.': 'Ženski spol',
            's': 'Srednji spol', 's mn.': 'Srednji spol',
        }

        gesla = self.slovar.xpath('//geslo[BV/samostalnik]')
        for geslo in gesla:
            try:
                iztocnica = geslo.xpath('iztočnica/text()')[0]
                spol = geslo.xpath('BV/samostalnik/text()')[0]
                skupina = ime_skupine[spol]
                skupine[skupina].append(iztocnica)
            except Exception:
                pass
        
        return skupine

class NalogaRazvrstiVPreglednicoBesednaVrsta(NalogaRazvrstiVPreglednico):

    IME = 'Razvrsti v preglednico glede na besedno vrsto'
    NAVODILA = 'Navedenim besedam določi besedno vrsto in jih zapiši v ustrezno polje v preglednici.'
    
    def sestavi_skupine(self):

        skupine = { 'Samostalnik': [], 'Pridevnik': [], 'Glagol': [] }
        ime_skupine = { 'samostalnik': 'Samostalnik', 'pridevnik': 'Pridevnik', 'glagol': 'Glagol' }

        gesla = self.slovar.xpath('//geslo[BV]')
        for geslo in gesla:
            try:
                iztocnica = geslo.xpath('iztočnica/text()')[0]
                besedna_vrsta = geslo.xpath('BV')[0]
                besedna_vrsta = list(besedna_vrsta)[0].tag

                skupina = ime_skupine[besedna_vrsta]
                skupine[skupina].append(iztocnica)
            except Exception:
                pass
        
        return skupine