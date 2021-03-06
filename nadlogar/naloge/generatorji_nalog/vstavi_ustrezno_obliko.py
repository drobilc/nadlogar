from .generator_nalog import GeneratorNalogSolskiSlovar
from lxml import etree
import random

class NalogaVstaviUstreznoObliko(GeneratorNalogSolskiSlovar):

    IME = 'Vstavi ustrezno obliko besede'
    NAVODILA = 'Postavi besede v oklepajih v ustrezno obliko in z njimi dopolni povedi.'
    
    def generiraj_primere(self, stevilo_primerov=6):
        self.zgledi = self.slovar.xpath('//geslo/pomen/S-zgled')
        random.shuffle(self.zgledi)
        self.indeks = 0

        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        zgled = self.zgledi[self.indeks]
        self.indeks += 1

        geslo = zgled.getparent().getparent()
        iztocnica = geslo.xpath('iztočnica')[0].text
        
        # Vsak zgled vsebuje oznaceno iztocnico v tagu <i>iztocnica</i>. Ta se lahko pojavi tudi veckrat.
        # Odstranimo vse primere, kjer se to zgodi, saj zelimo le naloge, kjer uporabniki vpisujejo eno besedo.
        iztocnice_zgleda = zgled.xpath('i')
        if len(iztocnice_zgleda) != 1:
            return self.generiraj_primer()

        # Najdemo obliko iztocnice v zgledu (pravilno rešitev)
        iztocnica_zgleda = iztocnice_zgleda[0].text    
        zgled_besedilo = etree.tostring(zgled, method='text', encoding='unicode')
        
        # print(zgled_besedilo.replace(iztocnica_zgleda, '______ ({})'.format(iztocnica)))
        try:
            pred, po = zgled_besedilo.split(iztocnica_zgleda)
            return {'pred': pred, 'iztocnica': iztocnica, 'po': po, 'resitev': iztocnica_zgleda}
        except Exception:
            return self.generiraj_primer()