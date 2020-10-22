from .generator_nalog import GeneratorNalog
from .izloci_vsiljivca import *
from .vstavi_ustrezno_obliko import *
from .doloci_slovnicno_stevilo import *
from .stevilo_pomenov import *
from .vsiljivec_glas import *
from .poisci_ustreznico_spol import *

GENERATORJI = [
    NalogaIzlociVsiljivcaSpol,
    NajdiVsiljivcaBesednaVrsta,
    NajdiVsiljivcaStevilo,
    NajdiVsiljivcaPredmetnoPodrocje,
    NalogaVstaviUstreznoObliko,
    
    NalogaRazvrstiVPreglednico,
    NalogaRazvrstiVPreglednicoStevilo,
    NalogaRazvrstiVPreglednicoSpol,
    NalogaRazvrstiVPreglednicoBesednaVrsta,

    NalogaDolociSteviloPomenov,
    NalogaGlasVsiljivec,
    NalogaPoisciZenskoUstreznico,
    NalogaPoisciMoskoUstreznico
]