from ..generatorji_nalog import *
from ..models import Test

class Visitor(object):
    def visit(self, visitable, argument=None):
        if isinstance(visitable, Test):
            return self.visit_test(visitable, argument)
        elif isinstance(visitable, GeneratorNalog):
            return self.visit_naloga(visitable, argument)
        raise ValueError('visitable must be a subclass of Test or GeneratorNalog')
    
    def visit_test(self, test: Test, argument):
        raise NotImplementedError
    
    def visit_naloga(self, naloga: GeneratorNalog, argument):
        raise NotImplementedError
