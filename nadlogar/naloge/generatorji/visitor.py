from ..naloge.test import Test
from ..naloge.naloga import Naloga

class Visitor(object):
    def visit(self, visitable, argument=None):
        if isinstance(visitable, Test):
            return self.visit_test(visitable, argument)
        elif isinstance(visitable, Naloga):
            return self.visit_naloga(visitable, argument)
        raise ValueError('visitable must be a subclass of Test or Naloga')
    
    def visit_test(self, test: Test, argument):
        raise NotImplementedError
    
    def visit_naloga(self, naloga: Naloga, argument):
        raise NotImplementedError
