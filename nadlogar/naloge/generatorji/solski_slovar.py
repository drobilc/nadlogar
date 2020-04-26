from lxml import etree

class SolskiSlovarGenerator(object):

    def __init__(self):
        # Odpremo solski slovar in si v objekt shranimo koren xml drevesa DOC
        with open('slovarji/solski_slovar.xml', 'r', encoding='utf-8') as slovar:
            self.slovar = etree.parse(slovar)
    
    def generiraj_primere(self, n):
        raise NotImplementedError