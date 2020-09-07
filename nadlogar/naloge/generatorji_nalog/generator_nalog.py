class GeneratorNalog(object):

    def __init__(self):
        pass

    def generiraj_primere(self, stevilo_primerov=6):
        return [self.generiraj_primer() for i in range(stevilo_primerov)]
    
    def generiraj_primer(self):
        return {}

    def accept(self, visitor, argument=None):
        return visitor.visit(self, argument)