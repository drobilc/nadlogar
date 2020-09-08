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
        generirano_drevo = html_generator.visit_naloga(naloga, None)
        return tostring(generirano_drevo, xml_declaration=False, encoding='utf-8')
    
    def visit_naloga(self, naloga, argument):
        if isinstance(naloga, NalogaIzlociVsiljivca):
            return self.visit_izloci_vsiljivca_naloga(naloga)
        elif isinstance(naloga, NalogaVstaviUstreznoObliko):
            return self.visit_vstavi_ustrezno_obliko_naloga(naloga)
        elif isinstance(naloga, NalogaDolociSlovnicnoStevilo):
            return self.visit_doloci_slovnicno_stevilo_naloga(naloga)
        elif isinstance(naloga, NalogaDolociSteviloPomenov):
            return self.visit_stevilo_pomenov_naloga(naloga)
        elif isinstance(naloga, NalogaGlasVsiljivec):
            return self.visit_glas_vsiljivec_naloga(naloga)
        return None
    
    def visit_izloci_vsiljivca_naloga(self, naloga: NalogaIzlociVsiljivca):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)
        
        seznam_primerov = etree.SubElement(html, 'ul')
        for primer in naloga.primeri():
                primer_element = etree.SubElement(seznam_primerov, 'li')
                primer_element.text = ', '.join(primer['besede'])

        return html
    
    def visit_vstavi_ustrezno_obliko_naloga(self, naloga: NalogaVstaviUstreznoObliko):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)
        
        seznam_primerov = etree.SubElement(html, 'ul')
        for primer in naloga.primeri():
            primer_element = etree.SubElement(seznam_primerov, 'li')
            primer_tekst = '{} __________ ({}) {}'.format(primer['pred'], primer['iztocnica'], primer['po'])
            primer_element.text = primer_tekst

        return html
    
    def visit_doloci_slovnicno_stevilo_naloga(self, naloga: NalogaDolociSlovnicnoStevilo):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)
        return html
    
    def visit_stevilo_pomenov_naloga(self, naloga: NalogaDolociSteviloPomenov):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)
        return html
    
    def visit_glas_vsiljivec_naloga(self, naloga: NalogaGlasVsiljivec):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)
        return html