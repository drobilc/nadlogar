from django import forms

from .visitor import Visitor
from ..generatorji_nalog import *
from ..models import DelovniList

class StandardnaForma(forms.Form):
    stevilo_primerov = forms.IntegerField(label='Število primerov')
    navodila = forms.CharField(label='Navodila', widget=forms.Textarea(attrs={ 'rows' : 3 }))

class GlasVsiljivecForma(StandardnaForma):
    stevilo_primerov = None
    beseda = forms.CharField(label='Rešitev')

class ObrazecGenerator(Visitor):
    
    @staticmethod
    def generiraj_obrazec(naloga: GeneratorNalog):
        # Osnovni podatki naloge, ki se lahko uporabijo za zapolnjevanje vsebine
        # obrazca.
        podatki = {
            'navodila': naloga.navodila,
            'stevilo_primerov': naloga.stevilo_primerov
        }

        if isinstance(naloga, NalogaGlasVsiljivec):
            podatki['beseda'] = naloga.podatki['beseda']
            return GlasVsiljivecForma(initial=podatki)
        
        return StandardnaForma(initial=podatki)