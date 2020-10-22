from .visitor import Visitor
from ..generatorji_nalog import *
from ..models import DelovniList

from lxml import etree
from lxml.etree import tostring

class HtmlGenerator(Visitor):
    
    @staticmethod
    def generiraj_html(naloga):
        html_generator = HtmlGenerator()
        generirano_drevo = html_generator.visit_naloga(naloga, None)
        return tostring(generirano_drevo, xml_declaration=False, encoding='utf-8')
    
    def visit_naloga(self, naloga, argument):
        # Pri vsaki nalogi najprej ustvarimo HTML element 'div', v katerega bomo
        # vstavili vse podatke o nalogi
        naloga_html = etree.Element('div')

        # Nato vanj dodamo navodila naloge
        navodila_element = etree.SubElement(naloga_html, 'p')
        navodila_element.text = naloga.navodila
        navodila_element.set('class', 'navodila')

        generator = naloga.generator_nalog()

        # Odvisno od tipa naloge sestavimo seznam primerov
        if isinstance(generator, NalogaIzlociVsiljivca):
            self.visit_izloci_vsiljivca_naloga(naloga, generator, naloga_html)

        elif isinstance(generator, NalogaVstaviUstreznoObliko):
            self.visit_vstavi_ustrezno_obliko_naloga(naloga, generator, naloga_html)

        elif isinstance(generator, NalogaRazvrstiVPreglednico):
            self.visit_razvrsti_v_preglednico_naloga(naloga, generator, naloga_html)

        elif isinstance(generator, NalogaDolociSteviloPomenov):
            self.visit_stevilo_pomenov_naloga(naloga, generator, naloga_html)

        elif isinstance(generator, NalogaGlasVsiljivec):
            self.visit_glas_vsiljivec_naloga(naloga, generator, naloga_html)
        
        elif isinstance(generator, NalogaPoisciZenskoUstreznico):
            self.visit_poisci_zensko_ustreznico_naloga(naloga, generator, naloga_html)
        
        elif isinstance(generator, NalogaPoisciMoskoUstreznico):
            self.visit_poisci_mosko_ustreznico_naloga(naloga, generator, naloga_html)

        return naloga_html
    
    def _ustvari_seznam_primerov(self, naloga_html):
        seznam_primerov = etree.SubElement(naloga_html, 'ul')
        seznam_primerov.set('class', 'primeri')
        return seznam_primerov
    
    def _ustvari_primer(self, seznam_primerov, tag='li', text=None, razredi=[], prikazi_krizec=True):
        primer = etree.SubElement(seznam_primerov, tag)
        if text is not None:
            primer.text = text
        
        vsi_razredi = razredi + ['primer']
        primer.set('class', ' '.join(vsi_razredi))

        if prikazi_krizec:
            odstrani_primer = etree.SubElement(primer, 'div', {'class': 'odstrani-primer'})
            odstrani_primer.text = '×'

        return primer
    
    def _ustvari_element_tekst(self, stars, tag='p', tekst=None):
        element = etree.SubElement(stars, tag)
        element.text = tekst
        return element
    
    def visit_izloci_vsiljivca_naloga(self, naloga, generator: NalogaIzlociVsiljivca, naloga_html):        
        seznam_primerov = self._ustvari_seznam_primerov(naloga_html)
        for primer in naloga.primeri():
                primer_element = self._ustvari_primer(seznam_primerov)
                primer_element.text = ', '.join(primer['besede'])

        return seznam_primerov
    
    def visit_vstavi_ustrezno_obliko_naloga(self, naloga, generator: NalogaVstaviUstreznoObliko, naloga_html):       
        seznam_primerov = self._ustvari_seznam_primerov(naloga_html)
        for primer in naloga.primeri():
            primer_element = self._ustvari_primer(seznam_primerov)

            self._ustvari_element_tekst(primer_element, 'span', primer['pred'])

            prazen_prostor = etree.SubElement(primer_element, 'span')
            prazen_prostor.text = '______________'

            self._ustvari_element_tekst(primer_element, 'span', ' ({})'.format(primer['iztocnica']))
            self._ustvari_element_tekst(primer_element, 'span', primer['po'])

        return seznam_primerov
    
    def visit_razvrsti_v_preglednico_naloga(self, naloga, generator, naloga_html):
        seznam_primerov = self._ustvari_seznam_primerov(naloga_html)
        for primer in naloga.primeri():

            tabela = etree.Element('table')
            tabela.set('class', 'table mt-2 table-bordered')
            naslovna_vrstica = etree.SubElement(tabela, 'tr')
            ostale_vrstice = etree.SubElement(tabela, 'tr')
            for skupina in primer['skupine']:
                self._ustvari_element_tekst(naslovna_vrstica, 'th', skupina)
                etree.SubElement(ostale_vrstice, 'td')
            ostale_vrstice.set('style', 'height: 100px')

            primer_element = self._ustvari_primer(seznam_primerov, razredi=['mt-3'])
            primer_element.text = ', '.join(primer['besede'])
            primer_element.append(tabela)

        return seznam_primerov
    
    def visit_stevilo_pomenov_naloga(self, naloga, generator: NalogaDolociSteviloPomenov, naloga_html):
        seznam_primerov = self._ustvari_seznam_primerov(naloga_html)
        for primer in naloga.primeri():
            primer_element = self._ustvari_primer(seznam_primerov)
            
            primer_podatki_element = etree.SubElement(primer_element, 'div')
            primer_podatki_element.set('class', 'd-flex')

            iztocnica_element = etree.SubElement(primer_podatki_element, 'div')
            iztocnica_element.text = primer['beseda']
            iztocnica_element.set('class', 'w-25')   

            vsebnik = etree.SubElement(primer_podatki_element, 'div')
            vsebnik.set('class', 'w-25 d-flex justify-content-between')
            for i in range(1, 5):
                self._ustvari_element_tekst(vsebnik, 'span', str(i))         

        return seznam_primerov
    
    def visit_glas_vsiljivec_naloga(self, naloga, generator: NalogaGlasVsiljivec, naloga_html):
        vsebnik = etree.SubElement(naloga_html, 'div')

        for primer in naloga.primeri():
            primer_element = self._ustvari_primer(vsebnik, 'div', prikazi_krizec=False)
            vrstica = etree.SubElement(primer_element, 'div')
            vrstica.set('class', 'w-50 d-flex justify-content-around mx-auto text-monospace border-bottom p-1')
            for glas in primer['glasovi']:
                self._ustvari_element_tekst(vrstica, 'span', glas)

        return vsebnik

    
    def visit_poisci_zensko_ustreznico_naloga(self, naloga, generator: NalogaPoisciZenskoUstreznico, naloga_html):
        seznam_primerov = self._ustvari_seznam_primerov(naloga_html)
        for primer in naloga.primeri():
            primer_element = self._ustvari_primer(seznam_primerov)
            self._ustvari_element_tekst(primer_element, 'span', primer['maskulinativ'])
            self._ustvari_element_tekst(primer_element, 'span', ' - ____________________')
            
        return seznam_primerov
    
    def visit_poisci_mosko_ustreznico_naloga(self, naloga, generator: NalogaPoisciZenskoUstreznico, naloga_html):
        seznam_primerov = self._ustvari_seznam_primerov(naloga_html)
        for primer in naloga.primeri():
            primer_element = self._ustvari_primer(seznam_primerov)
            self._ustvari_element_tekst(primer_element, 'span', primer['feminativ'])
            self._ustvari_element_tekst(primer_element, 'span', ' - ____________________')
            
        return seznam_primerov