from .generator_nalog import GeneratorNalog
from .izloci_vsiljivca import *
from .vstavi_ustrezno_obliko import NalogaVstaviUstreznoObliko
from .doloci_slovnicno_stevilo import NalogaDolociSlovnicnoStevilo
from .stevilo_pomenov import NalogaDolociSteviloPomenov
from .vsiljivec_glas import NalogaGlasVsiljivec
from .poisci_ustreznico_spol import NalogaPoisciZenskoUstreznico, NalogaPoisciMoskoUstreznico

GENERATORJI = [
    NalogaIzlociVsiljivcaSpol,
    NajdiVsiljivcaBesednaVrsta,
    NajdiVsiljivcaStevilo,
    NajdiVsiljivcaPredmetnoPodrocje,
    NalogaVstaviUstreznoObliko,
    NalogaDolociSlovnicnoStevilo,
    NalogaDolociSteviloPomenov,
    NalogaGlasVsiljivec,
    NalogaPoisciZenskoUstreznico,
    NalogaPoisciMoskoUstreznico
]