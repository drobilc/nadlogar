class GeneratorNalog(object):

    def __init__(self, podatki, navodila=None, stevilo_primerov=6):
        self.podatki = podatki
        self.navodila = navodila
        self.stevilo_primerov = stevilo_primerov
    
    def generiraj_nalogo(self):
        """Funkcija generiraj_nalogo se klice kadar je v bazi podatkov
        ustvarjena nova naloga ali kadar je potrebno nalogo ponovno ustvariti.
        Pri klicu ustvarimo slovar "podatki", ki se nato kot JSON shrani v bazo
        podatkov in se uporablja za obnovitev seznama primerov naloge."""
        # Sestavimo seznam novih primerov. Vsak primer je slovar, ki vsebuje
        # poljubne podatke s pomocjo katerih ga znata Latex in HTML generator
        # prikazati in nato vrnemo slovar podatkov naloge
        novi_primeri = self.generiraj_primere(self.stevilo_primerov)
        return { 'primeri': novi_primeri }

    
    def primeri(self):
        # Ce naloga se ni generirana, bo self.podatki zasedla vrednost None, v
        # tem primeru zgeneriramo seznam primerov in ga vrnemo
        if self.podatki is None:
            self.podatki = self.generiraj_nalogo()
        
        return self.podatki['primeri']

    def generiraj_primere(self, stevilo_primerov=6):
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        return {}

    def accept(self, visitor, argument=None):
        return visitor.visit(self, argument)