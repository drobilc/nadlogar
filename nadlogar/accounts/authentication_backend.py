from django.contrib.auth.backends import BaseBackend
from naloge.models import Uporabnik
from accounts.francek import *
from django.conf import settings

class FrancekBackend(BaseBackend):

    # FrancekBackend deluje kot sekundarni nacin prijave v aplikacijo. V
    # nastavitvah mora biti na zadnjem mestu - kot v naslednjem primeru.
    # AUTHENTICATION_BACKENDS = [
    #   'django.contrib.auth.backends.ModelBackend',
    #   'accounts.authentication_backend.FrancekBackend'
    # ]

    # Deluje tako, da poskusa uporabnika prijaviti v njegov Francek racun. Ce je
    # prijava uspesna, ustvari v Djangovi bazi podatkov nov uporabniski racun in
    # mu nastavi uporabnisko ime in geslo.

    # Pri naslednji prijavi Django najprej preveri ali ze pozna kaksnega
    # uporabnika z vnesenimi podatki, sicer pa uporabi ta backend. Ce uporabnik
    # na francku spremeni geslo, bo prvi (djangov) backend za prijavo vrnil, da
    # uporabnika se nima in sprozil franckov backend.


    def authenticate(self, request, username=None, password=None):
        francek_api = FrancekApiTest(settings.FRANCEK_API_KEY)

        try:
            francek_uporabnik = francek_api.link_account(username, password)
        except Exception:
            # Ce je pri prijavi s Franckom prislo do napake, uporabnik ne
            # obstaja in vrnemo None
            return None
        
        # Preverimo, ali uporabnik z vnesenim uporabniskim imenom ze obstaja v
        # bazi. Ce obstaja, to najverjetneje pomeni, da si je uporabnik na
        # Francku spremenil geslo, a se podatki v nasi aplikaciji se niso
        # posodobili. Popravimo podatke.
        try:
            uporabnik = Uporabnik.objects.get(username=username)
        except Uporabnik.DoesNotExist:
            uporabnik = Uporabnik(username=username)
        
        # Uporabniku nastavimo is_staff na True, da se lahko prijavi v zaledje Djanga
        uporabnik.is_staff = True
        # Popravimo geslo uporabniku in ga shranimo
        uporabnik.set_password(password)
        uporabnik.save()

        return uporabnik
    
    def get_user(self, user_id):
        try:
            return Uporabnik.objects.get(pk=user_id)
        except Uporabnik.DoesNotExist:
            return None