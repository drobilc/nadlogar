from django import forms

from .visitor import Visitor
from ..generatorji_nalog import *
from ..models import DelovniList, Naloga

class StandardnaForma(forms.Form):
    # Action polje je vedno prisotno in sporoci nasemu sistemu, da zeli
    # uporabnik urediti podatke naloge
    action = forms.CharField(widget=forms.HiddenInput())
    naloga_id = forms.IntegerField(widget=forms.HiddenInput())

    stevilo_primerov = forms.IntegerField(label='Število primerov')
    navodila = forms.CharField(label='Navodila', widget=forms.Textarea(attrs={ 'rows' : 3 }))

class GlasVsiljivecForma(StandardnaForma):
    stevilo_primerov = None
    beseda = forms.CharField(label='Rešitev')

class ObrazecGenerator(Visitor):
    
    @staticmethod
    def generiraj_obrazec(naloga: Naloga, request=None):
        post_podatki = None
        if request is not None and request.POST is not None:
            post_podatki = request.POST
        
        # Osnovni podatki naloge, ki se lahko uporabijo za zapolnjevanje vsebine
        # obrazca.
        podatki = {
            'action': 'uredi_nalogo',
            'naloga_id': naloga.id,
            'navodila': naloga.navodila,
            'stevilo_primerov': naloga.stevilo_primerov,
        }

        generator_nalog = naloga.generator_nalog()

        if isinstance(generator_nalog, NalogaGlasVsiljivec):
            podatki['beseda'] = naloga.podatki['beseda']
            return GlasVsiljivecForma(post_podatki, initial=podatki)
        
        return StandardnaForma(post_podatki, initial=podatki)