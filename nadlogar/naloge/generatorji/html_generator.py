from .visitor import Visitor
from ..generatorji_nalog import *
from ..models import DelovniList

from lxml import etree
from lxml.etree import tostring

# Sposojeno iz https://stackoverflow.com/questions/33386943/python-lxml-subelement-with-text-value
def subelement_with_text(_parent, _tag, attrib={}, _text=None, nsmap=None, **_extra):
    result = etree.SubElement(_parent, _tag, attrib, nsmap, **_extra)
    result.text = _text
    return result

def ustvari_primer(_parent, _tag, attrib={}, _text=None, _classes=[], nsmap=None, **_extra):
    result = etree.SubElement(_parent, _tag, attrib, nsmap, **_extra)

    razredi = _classes + ['primer']
    result.set('class', ' '.join(razredi))

    odstrani_primer = etree.SubElement(result, 'div')
    odstrani_primer.set('class', 'odstrani-primer')
    
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
                primer_element = ustvari_primer(seznam_primerov, 'li')
                primer_element.text = ', '.join(primer['besede'])

        return html
    
    def visit_vstavi_ustrezno_obliko_naloga(self, naloga: NalogaVstaviUstreznoObliko):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)
        
        seznam_primerov = etree.SubElement(html, 'ul')
        for primer in naloga.primeri():
            primer_element = ustvari_primer(seznam_primerov, 'li')
            primer_tekst = '{} __________ ({}) {}'.format(primer['pred'], primer['iztocnica'], primer['po'])
            primer_element.text = primer_tekst

        return html
    
    def visit_doloci_slovnicno_stevilo_naloga(self, naloga: NalogaDolociSlovnicnoStevilo):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)

        seznam_primerov = etree.SubElement(html, 'ul')
        for primer in naloga.primeri():

            tabela = etree.Element('table')
            tabela.set('class', 'table mt-2 table-bordered')
            naslovna_vrstica = etree.SubElement(tabela, 'tr')
            subelement_with_text(naslovna_vrstica, 'th', _text='Ednina')
            subelement_with_text(naslovna_vrstica, 'th', _text='Dvojina')
            subelement_with_text(naslovna_vrstica, 'th', _text='Množina')
            ostale_vrstice = etree.SubElement(tabela, 'tr')
            etree.SubElement(ostale_vrstice, 'td')
            etree.SubElement(ostale_vrstice, 'td')
            etree.SubElement(ostale_vrstice, 'td')
            ostale_vrstice.set('style', 'height: 100px')

            primer_element = ustvari_primer(seznam_primerov, 'li', _classes=['mt-3'])
            primer_element.text = ', '.join(primer['besede'])
            primer_element.append(tabela)

        return html
    
    def visit_stevilo_pomenov_naloga(self, naloga: NalogaDolociSteviloPomenov):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)

        tabela = etree.SubElement(html, 'table')
        for primer in naloga.primeri():
            vrstica = ustvari_primer(tabela, 'tr')
            subelement_with_text(vrstica, 'td', _text=primer['beseda'])

            for i in range(1, 5):
                subelement_with_text(vrstica, 'td', _text=str(i), style='width: 50px; text-align: center;')

        return html
    
    def visit_glas_vsiljivec_naloga(self, naloga: NalogaGlasVsiljivec):
        html = etree.Element('div')
        subelement_with_text(html, 'p', _text=naloga.navodila)

        vsebnik = etree.SubElement(html, 'div', style='text-align: center;')

        tabela = etree.SubElement(vsebnik, 'table')
        tabela.set('class', 'table table-bordered')
        for primer in naloga.primeri():
            vrstica = ustvari_primer(tabela, 'tr')
            for glas in primer['glasovi']:
                subelement_with_text(vrstica, 'td', _text=glas)

        return html