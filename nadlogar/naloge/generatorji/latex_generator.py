from .visitor import Visitor
from ..generatorji_nalog import *
from ..models import DelovniList

import string

from pylatex import Document, Command, Tabular, Center
from pylatex.utils import italic, NoEscape
from pylatex.base_classes import Options
from pylatex.basic import NewLine

def remove_newlines(text):
    return text.replace('\r\n', ' ').replace('\n', ' ')

class LatexGenerator(object):

    def generatorji_nalog(self):
        # Pri dodajanju novih nalog je potrebno dodati preslikavo med novim
        # razredom in funkcijo, ki zna zgenerirati latex za tak tip naloge.

        # Za vsak RAZRED generatorja nalog vrnemo funkcijo, ki zna generirati
        # nalogo takega tipa. Ce naloge ni v slovarju, se naloga ne bo
        # generirala (oziroma se bo zgeneriralo le navodilo).
        return {
            # Naloge tipa izloci vsiljivca
            NalogaIzlociVsiljivcaSpol: self._generiraj_nalogo_izloci_vsiljivca,
            NajdiVsiljivcaBesednaVrsta: self._generiraj_nalogo_izloci_vsiljivca,
            NajdiVsiljivcaStevilo: self._generiraj_nalogo_izloci_vsiljivca,
            NajdiVsiljivcaPredmetnoPodrocje: self._generiraj_nalogo_izloci_vsiljivca,

            # Naloge tipa vstavi ustrezno obliko besede
            NalogaVstaviUstreznoObliko: self._generiraj_nalogo_vstavi_ustrezno_obliko,

            # Naloge tipa doloci slovnicno stevilo
            NalogaDolociSlovnicnoStevilo: self._generiraj_nalogo_doloci_slovnicno_stevilo,

            # Naloge tipa doloci stevilo pomenov v slovarju Francek
            NalogaDolociSteviloPomenov: self._generiraj_nalogo_doloci_stevilo_pomenov,

            # Naloge tipa izloci vsiljivca glede na glas (samoglasniki / soglasniki)
            NalogaGlasVsiljivec: self._generiraj_nalogo_izloci_vsiljivca_glas,

            # Naloge tipa poisci mosko / zensko ustreznico
            NalogaPoisciZenskoUstreznico: self._generiraj_nalogo_poisci_zensko_ustreznico,
            NalogaPoisciMoskoUstreznico: self._generiraj_nalogo_poisci_mosko_ustreznico,
        }

    @staticmethod
    def generiraj_latex_dokument(delovni_list: DelovniList):
        generator = LatexGenerator()
        latex_dokument = generator._generiraj_latex_dokument(delovni_list)
        return latex_dokument

    def _generiraj_latex_dokument(self, delovni_list: DelovniList):
        latex_dokument = Document()
        # Dokumentu nastavimo razred `izpit`, ki vsebuje ukaze za naloge,
        # primere in podobno.
        latex_dokument.documentclass = Command('documentclass', 'izpit')

        # Dokument je potrebno zaceti z ukazmo izpit, ki mu dodamo naslov in
        # opis (navodila) delovnega lista.
        ukaz_izpit = Command('izpit',
            arguments=[remove_newlines(delovni_list.naslov), '', remove_newlines(delovni_list.opis)],
            options=Options('brez vpisne', naloge=0)
        )
        latex_dokument.append(ukaz_izpit)

        # Ko smo dodali ukaz za izpit, se sprehodimo cez vse naloge in
        # generiramo latex zanje
        for naloga in delovni_list.naloge.all():
            # Generiramo ukaze za doloceno nalogo
            naloga_ukazi = self.generiraj_latex_za_nalogo(naloga, latex_dokument)
            # Dodamo ukaze v latex dokument
            latex_dokument.extend(naloga_ukazi)

        return latex_dokument
    
    def generiraj_latex_za_nalogo(self, naloga, latex_dokument):
        # Vrsto naloge lahko identificiramo glede na njen atribut `generator`.
        # Ker zelimo, da je izgled dokumenta vsaj kolikor toliko homogen, bomo
        # vsem nalogam zgenerirali enaka navodila.
        naloga_navodila = [
            Command('naloga', arguments=[remove_newlines(naloga.navodila)])
        ]

        # Glede na tip naloge poklicemo ustrezno funkcijo, ki zna zgenerirati
        # latex za primere te naloge
        naloga_ukazi = []

        # Najprej iz naloge pridobimo razred generatorja. Slovar
        # vsi_generatorji_nalog nam pove katera funkcija se mora izvesti, ce
        # zelimo generirati vsebino dolocenega tipa naloge. Ce se razred naloge
        # nahaja v slovarju vsi_generatorji_nalog poklicemo funkcijo in rezultat
        # shranimo v seznam naloga_ukazi.
        generator_razred = naloga.generator_nalog_razred()
        vsi_generatorji_nalog = self.generatorji_nalog()
        if generator_razred in vsi_generatorji_nalog:
            # Poiscemo funkcijo, ki se mora izvesti ce zelimo generirati vsebino
            # trenutne naloge
            generiraj_latex_za_nalogo_funkcija = vsi_generatorji_nalog[generator_razred]

            # Zgeneriramo latex ukaze za trenutno nalogo
            generirani_ukazi = generiraj_latex_za_nalogo_funkcija(naloga, latex_dokument)
            naloga_ukazi.extend(generirani_ukazi)

        # Zdruzimo tabeli navodil in ukazov naloge in ju vrnemo
        return naloga_navodila + naloga_ukazi
    
    def _generiraj_nalogo_izloci_vsiljivca(self, naloga, latex_dokument):
        primeri = []
        for primer in naloga.primeri():
            primeri.append(Command('podnaloga'))
            for beseda in primer['besede']:
                primeri.append(beseda)
                primeri.append(Command('qquad'))
        
        # Ker ne zelimo se dodatnega prostora na desni strani zadnje besede,
        # zadnji ukaz '\quad' odstranimo iz generiranega seznama primerov
        return primeri[:-1]
    
    def _generiraj_nalogo_vstavi_ustrezno_obliko(self, naloga, latex_dokument):
        primeri = []
        for primer in naloga.primeri():
            primeri.append(Command('podnaloga'))

            # Ce je v primer['po'] simbol (pika, vprasaj, klicaj, ...) je
            # potrebno odstraniti zadnji presledek v ' ({}) '
            iztocnica_niz = ' ({}) '.format(primer['iztocnica'])
            po = primer['po'].lstrip().lower()
            if len(po) > 0 and po[0] not in string.ascii_lowercase:
                iztocnica_niz = iztocnica_niz.rstrip()

            primeri.extend([
                primer['pred'],
                '________________ ',
                iztocnica_niz,
                primer['po']
            ])

        return primeri
    
    def _generiraj_nalogo_doloci_slovnicno_stevilo(self, naloga, latex_dokument):

        prostor = Command('vspace', arguments=['4cm'])

        center = Center()
        with center.create(Tabular('|p{4cm}|p{4cm}|p{4cm}|')) as tabela:
            tabela.add_hline()
            tabela.add_row(('EDNINA', 'DVOJINA', 'MNOŽINA'))
            tabela.add_hline()
            tabela.add_row((prostor, '', ''))
            tabela.add_hline()

        primeri = []
        for primer in naloga.primeri():
            primeri.append(Command('podnaloga'))
            primeri.extend([', '.join(primer['besede'])])
            primeri.append(Command('vspace', ['0.5cm']))
            primeri.append(center)
            primeri.append(Command('vspace', ['0.5cm']))

        return primeri
    
    def _generiraj_nalogo_doloci_stevilo_pomenov(self, naloga, latex_dokument):
        primeri = []

        maksimalno_stevilo_pomenov = max([p['stevilo_pomenov'] for p in naloga.primeri()])
        maksimalno_stevilo_pomenov = max(maksimalno_stevilo_pomenov, 4)

        for primer in naloga.primeri():
            primeri.append(Command('podnaloga'))
            primeri.append(Command('makebox[3cm]', arguments=[primer['beseda']], options=['l']))
            for i in range(1, maksimalno_stevilo_pomenov + 1):
                primeri.append(Command('qquad'))
                primeri.append(i)

        return primeri
    
    def _generiraj_nalogo_izloci_vsiljivca_glas(self, naloga, latex_dokument):
        
        center = Center()
        with center.create(Tabular('ccccc')) as tabela:
            for primer in naloga.primeri():
                tabela.add_hline()
                tabela.add_row(primer['glasovi'])
            tabela.add_hline()
        
        return [center]
    
    def _generiraj_nalogo_poisci_zensko_ustreznico(self, naloga, latex_dokument):
        primeri = []
        for primer in naloga.primeri():
            primeri.append(Command('podnaloga'))
            primeri.extend([
                primer['maskulinativ'],
                Command('hspace', '10pt'),
                '-',
                Command('hspace', '10pt'),
                '____________________'
            ])
        return primeri
    
    def _generiraj_nalogo_poisci_mosko_ustreznico(self, naloga, latex_dokument):
        primeri = []
        for primer in naloga.primeri():
            primeri.append(Command('podnaloga'))
            primeri.extend([
                primer['feminativ'],
                Command('hspace', '10pt'),
                '-',
                Command('hspace', '10pt'),
                '____________________'
            ])
        return primeri