from .models import Bestellung, BestellteArtikel
import json

def warenkorb_anzahl(request):

    if request.user.is_authenticated:
        kunde = request.user.kunde
        
        # get_or_create separiert 
        # bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        bestellung = Bestellung.objects.filter(kunde=kunde, erledigt=False).first()
        if not bestellung:
            bestellung = Bestellung.objects.create(kunde=kunde, erledigt=False)

        if bestellung:
            menge = bestellung.get_gesamtmenge
        else:
            menge = 0
    # wenn User kein eingeloggter Kunde ist:
    else:
    # -> Auslesen des warenkorb-Cookies 
    # gibt es kein warenkorb-Cookie, dann soll ein leerer warenkorb erzeugt werden
        menge = 0
        try:
            warenkorb = json.loads(request.COOKIES['warenkorb'])
        except:
            warenkorb = {}
        for i in warenkorb:
            menge += warenkorb[i]["menge"]

    return {'menge': menge}
