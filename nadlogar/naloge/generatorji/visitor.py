from ..generatorji_nalog import *
from ..models import DelovniList

class Visitor(object):
    def visit(self, visitable, argument=None):
        if isinstance(visitable, DelovniList):
            return self.visit_test(visitable, argument)
        elif isinstance(visitable, GeneratorNalog):
            return self.visit_naloga(visitable, argument)
        raise ValueError('visitable must be a subclass of DelovniList or GeneratorNalog')
    
    def visit_test(self, test: DelovniList, argument):
        raise NotImplementedError
    
    def visit_naloga(self, naloga: GeneratorNalog, argument):
        raise NotImplementedError
