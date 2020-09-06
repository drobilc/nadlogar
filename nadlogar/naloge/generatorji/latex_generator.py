from .visitor import Visitor
from ..naloge import *

from pylatex import Document, Command, Tabular, Center
from pylatex.utils import italic, NoEscape
from pylatex.base_classes import Options
from pylatex.basic import NewLine

class LatexGenerator(Visitor):
    
    @staticmethod
    def generate_latex(test: Test):
        latex_document = Document()
        latex_document.documentclass = Command('documentclass', 'izpit')

        result = LatexGenerator().visit(test, latex_document)
        for element in result:
            latex_document.append(element)
        return latex_document

    def visit_test(self, test: Test, latex_document):
        datum = test.datum if test.datum is not None else Command('today')
        ukaz_izpit = Command('izpit',
            arguments=[test.naslov, datum, test.opis],
            options=Options('brez vpisne', naloge=0)
        )
        latex_ukazi = [ukaz_izpit]
        for naloga in test.naloge:
            latex_ukazi.extend(naloga.accept(self, latex_document))
        return latex_ukazi
    
    def visit_naloga(self, naloga: Naloga, latex_document):
        if isinstance(naloga, NalogaIzlociVsiljivca):
            return self.visit_izloci_vsiljivca_naloga(naloga, latex_document)
        elif isinstance(naloga, NalogaVstaviUstreznoObliko):
            return self.visit_vstavi_ustrezno_obliko_naloga(naloga, latex_document)
        elif isinstance(naloga, NalogaDolociSlovnicnoStevilo):
            return self.visit_doloci_slovnicno_stevilo_naloga(naloga, latex_document)
        elif isinstance(naloga, NalogaDolociSteviloPomenov):
            return self.visit_stevilo_pomenov_naloga(naloga, latex_document)
        elif isinstance(naloga, NalogaGlasVsiljivec):
            return self.visit_glas_vsiljivec_naloga(naloga, latex_document)
        
        return [Command('naloga', arguments=[naloga.navodila])]
    
    def visit_izloci_vsiljivca_naloga(self, naloga: NalogaIzlociVsiljivca, latex_document):
        primeri = []
        for primer in naloga.primeri:
            primeri.append(Command('podnaloga'))
            for beseda in primer['besede']:
                primeri.append(beseda)
                primeri.append(Command('qquad'))

        return [Command('naloga', arguments=[naloga.navodila])] + primeri[:-1]
    
    def visit_vstavi_ustrezno_obliko_naloga(self, naloga: NalogaIzlociVsiljivca, latex_document):
        primeri = []
        for primer in naloga.primeri:
            primeri.append(Command('podnaloga'))
            primeri.extend([primer['pred'], '________', ' ({}) '.format(primer['iztocnica']), primer['po']])

        return [Command('naloga', arguments=[naloga.navodila])] + primeri
    
    def visit_doloci_slovnicno_stevilo_naloga(self, naloga: NalogaDolociSlovnicnoStevilo, latex_document):

        prostor = Command('vspace', arguments=['5cm'])

        center = Center()
        with center.create(Tabular('|p{4cm}|p{4cm}|p{4cm}|')) as tabela:
            tabela.add_hline()
            tabela.add_row(('EDNINA', 'DVOJINA', 'MNOŽINA'))
            tabela.add_hline()
            tabela.add_row((prostor, '', ''))
            tabela.add_hline()

        primeri = []
        for primer in naloga.primeri:
            primeri.append(Command('podnaloga'))
            primeri.extend([', '.join(primer['besede'])])
            primeri.append(Command('vspace', ['0.5cm']))
            primeri.append(center)
            primeri.append(Command('vspace', ['0.5cm']))

        return [Command('naloga', arguments=[naloga.navodila])] + primeri
    
    def visit_stevilo_pomenov_naloga(self, naloga: NalogaDolociSteviloPomenov, latex_document):
        primeri = []

        maksimalno_stevilo_pomenov = max([p['stevilo_pomenov'] for p in naloga.primeri])
        maksimalno_stevilo_pomenov = max(maksimalno_stevilo_pomenov, 4)

        for primer in naloga.primeri:
            primeri.append(Command('podnaloga'))
            primeri.append(Command('makebox[3cm]', arguments=[primer['beseda']], options=['l']))
            for i in range(1, maksimalno_stevilo_pomenov + 1):
                primeri.append(Command('qquad'))
                primeri.append(i)

        return [Command('naloga', arguments=[naloga.navodila])] + primeri
    
    def visit_glas_vsiljivec_naloga(self, naloga: NalogaDolociSteviloPomenov, latex_document):
        
        center = Center()
        with center.create(Tabular('|c|c|c|c|c|')) as tabela:
            for primer in naloga.primeri:
                tabela.add_hline()
                tabela.add_row(primer['glasovi'])
            tabela.add_hline()
        
        return [Command('naloga', arguments=[naloga.navodila])] + [center]