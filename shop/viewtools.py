import json
from . models import *

def gastCookie(request):
    try:
        warenkorb = json.loads(request.COOKIES['warenkorb'])
    except:
        warenkorb = {}

    artikels = []
    bestellung = {'get_gesamtpreis':0, 'get_gesamtmenge':0}
    menge = bestellung['get_gesamtmenge']

    for i in warenkorb:
        menge += warenkorb[i]["menge"]
        artikel = Artikel.objects.get(id=i)
        gesamtpreis = (artikel.preis * warenkorb[i]['menge'])
        bestellung['get_gesamtpreis'] += gesamtpreis
        bestellung['get_gesamtmenge'] += warenkorb[i]['menge']

        artikel = {
            'artikel':{
                'id':artikel.id,
                'name':artikel.name,
                'preis':artikel.preis,
                'bild':artikel.bild
            },
            'menge':warenkorb[i]['menge'],
            'get_summe':gesamtpreis
        }
        artikels.append(artikel)

    return{'artikels':artikels, 'bestellung':bestellung}

# ausgelagert aus views.py / bestellen
def gastBestellung(request, daten):
    name = daten['benutzerDaten']['name']
    email = daten['benutzerDaten']['email']

    cookieDaten = gastCookie(request)
    artikels = cookieDaten['artikels']

    # wenn ein Gast bereits mit eMail registriert ist, 
    # -> wird kein neuer Gastaccount mit gleicher eMail angelegt
    kunde, created = Kunde.objects.get_or_create(email=email)
    kunde.name = name
    kunde.save()

    bestellung = Bestellung.objects.create(kunde=kunde, erledigt=False)

    # Attribute s. models.py
    for i in artikels:
        artikel = Artikel.objects.get(id=i['artikel']['id'])
        # neue Var -> nimmmt jeden neuen bestellten Artikel auf 
        bestellteArtikel = BestellteArtikel.objects.create(
            artikel=artikel,
            bestellung=bestellung,
            menge=i['menge']
        )
    return kunde, bestellung
