from .generator_nalog import GeneratorNalog
import csv
import random
import os
from django.conf import settings

class NalogaPoisciZenskoUstreznico(GeneratorNalog):

    IME = 'Poišči žensko ustreznico'
    NAVODILA = 'Kako poimenujemo ženske, ki opravljajo določen poklic?'
    
    def generiraj_primere(self, stevilo_primerov=6):
        self.iztocnice = []
        pot_do_datoteke = os.path.join(settings.POT_DO_SLOVARJEV, 'maskulinativi_feminativi.csv')
        with open(pot_do_datoteke, 'r', encoding='utf-8-sig') as datoteka:
            bralec = csv.DictReader(datoteka, delimiter=';')
            for vrstica in bralec:
                self.iztocnice.append(vrstica)
        
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        izbor = random.choice(self.iztocnice)
        feminativi = [izbor['feminativ1'], izbor['feminativ2'], izbor['feminativ3']]
        feminativi = list(filter(lambda x: len(x) > 0, feminativi))
        return {'maskulinativ': izbor['maskulinativ'], 'feminativi': feminativi}

class NalogaPoisciMoskoUstreznico(GeneratorNalog):

    IME = 'Poišči moško ustreznico'
    NAVODILA = 'Poimenuj moške, ki opravljajo določen poklic.'
    
    def generiraj_primere(self, stevilo_primerov=6):
        self.iztocnice = []
        pot_do_datoteke = os.path.join(settings.POT_DO_SLOVARJEV, 'maskulinativi_feminativi.csv')
        with open(pot_do_datoteke, 'r', encoding='utf-8-sig') as datoteka:
            bralec = csv.DictReader(datoteka, delimiter=';')
            for vrstica in bralec:
                self.iztocnice.append(vrstica)
        
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        izbor = random.choice(self.iztocnice)
        return {'maskulinativ': izbor['maskulinativ'], 'feminativ': izbor['feminativ1']}