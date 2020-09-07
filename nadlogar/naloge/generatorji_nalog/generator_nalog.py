class GeneratorNalog(object):

    def __init__(self, podatki, navodila=None, stevilo_primerov=6):
        self.podatki = podatki
        self.navodila = navodila
        self.stevilo_primerov = stevilo_primerov

        # Ce so podatki null, jih zamenjamo s praznim slovarjem
        if self.podatki is None:
            self.podatki = {}
    
    def primeri(self):        
        if 'primeri' not in self.podatki:
            self.podatki['primeri'] = self.generiraj_primere(self.stevilo_primerov)
            print(self.podatki['primeri'])
        return self.podatki['primeri']

    def generiraj_primere(self, stevilo_primerov=6):
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        return {}

    def accept(self, visitor, argument=None):
        return visitor.visit(self, argument)