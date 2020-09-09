from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'naloge'
urlpatterns = [

    # Landing page, kjer se uporabniki seznanijo s produktom
    path('', views.index, name='index'),

    # Seznam vseh dokumentov dolocenega uporabnika
    path('dokumenti', views.seznam_dokumentov, name='seznam_dokumentov'),

    # Ustvarjanje novega dokumenta
    path('dokument/nov', views.ustvari_delovni_list, name='ustvari_delovni_list'),

    # Predogled dolocenega delovnega lista
    path('dokument/<int:id_delovnega_lista>', views.podrobnosti_delovnega_lista, name='podrobnosti_delovnega_lista'),

    # Urejanje delovnega lista
    path('dokument/<int:id_delovnega_lista>/uredi', views.urejanje_delovnega_lista, name='urejanje_delovnega_lista'),

    # Generiranje pdf dokumenta iz delovnega lista
    path('dokument/<int:id_delovnega_lista>/pdf', views.generiraj_delovni_list, name='generiraj_delovni_list'),

    # Dodajanje naloge na delovni list za Ajax zahteve
    path('dokument/<int:id_delovnega_lista>/dodaj_nalogo', views.dodaj_nalogo, name='dodaj_nalogo'),
    
    # Urejanje naloge iz delovnega lista za Ajax zahteve
    path('dokument/<int:id_delovnega_lista>/uredi_nalogo', views.uredi_nalogo, name='uredi_nalogo'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)