from .solski_slovar import SolskiSlovarGenerator

class VstaviUstreznoOblikoGenerator(SolskiSlovarGenerator):

    IME = 'Vstavi ustrezno obliko iztočnice'
    PREDLOGA = 'vstavi_ustrezno_obliko'
    NAVODILA = 'Postavi besede v ustrezno obliko in dopolni povedi.'
    
    def __init__(self):
        super().__init__()
    
    def generiraj_primere(self, n):
        generirani_primeri = []

        # Najdemo vse zglede v slovarju
        zgledi = self.slovar.xpath('//geslo/pomen/S-zgled')
        random.shuffle(zgledi)
        indeks = 0
        while len(generirani_primeri) < n:
            zgled = zgledi[indeks]
            indeks += 1

            geslo = zgled.getparent().getparent()
            iztocnica = geslo.xpath('iztočnica')[0].text
            
            # Vsak zgled vsebuje oznaceno iztocnico v tagu <i>iztocnica</i>. Ta se lahko pojavi tudi veckrat.
            # Odstranimo vse primere, kjer se to zgodi, saj zelimo le naloge, kjer uporabniki vpisujejo eno besedo.
            iztocnice_zgleda = zgled.xpath('i')
            if len(iztocnice_zgleda) != 1:
                continue

            # Najdemo obliko iztocnice v zgledu (pravilno rešitev)
            iztocnica_zgleda = iztocnice_zgleda[0].text    
            zgled_besedilo = etree.tostring(zgled, method='text', encoding='unicode')
            
            # print(zgled_besedilo.replace(iztocnica_zgleda, '______ ({})'.format(iztocnica)))
            pred, po = zgled_besedilo.split(iztocnica_zgleda)
            generirani_primeri.append({'pred': pred, 'iztocnica': iztocnica, 'po': po, 'resitev': iztocnice_zgleda})
        
        return generirani_primeri