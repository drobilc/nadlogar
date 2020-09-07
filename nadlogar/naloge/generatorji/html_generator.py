from .visitor import Visitor
from ..generatorji_nalog import *
from ..models import Test

from lxml import etree
from lxml.etree import tostring

# Sposojeno iz https://stackoverflow.com/questions/33386943/python-lxml-subelement-with-text-value
def subelement_with_text(_parent, _tag, attrib={}, _text=None, nsmap=None, **_extra):
    result = etree.SubElement(_parent, _tag, attrib, nsmap, **_extra)
    result.text = _text
    return result

class HtmlGenerator(Visitor):
    
    @staticmethod
    def generiraj_html(naloga):
        html_generator = HtmlGenerator()
        return html_generator.visit_naloga(naloga, None)
    
    def visit_naloga(self, naloga, argument):
        if isinstance(naloga, NalogaIzlociVsiljivca):
            return self.visit_izloci_vsiljivca_naloga(naloga)
        return None
    
    def visit_izloci_vsiljivca_naloga(self, naloga: NalogaIzlociVsiljivca):

        html = etree.Element('div')

        subelement_with_text(html, 'p', _text=naloga.navodila)
        
        seznam_primerov = etree.SubElement(html, 'ul')

        for primer in naloga.primeri():
                primer_element = etree.SubElement(seznam_primerov, 'li')
                primer_element.text = ', '.join(primer['besede'])

        return tostring(html, xml_declaration=False, encoding='utf-8')