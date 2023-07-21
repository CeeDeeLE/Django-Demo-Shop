from django.shortcuts import render, redirect
from django.contrib import messages

# login_required, um Seiten vor unberechtigtem Zugriff zu schützen
# Decorator wird mit @ ausgegeben
from django.contrib.auth.decorators import login_required

from . models import *
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth import authenticate, login, logout

# EigenesUserCreationForm basiert auf UserCreationForm von Django und ersetzt diese
# from django.contrib.auth.forms import UserCreationForm
from . forms import EigenesUserCreationForm

# für Bezahlvorgang -> Erstellung eindeutiger Auftrags-IDs
import uuid
# mark_safe zur Deklarierung einer ID als sicher
from django.utils.safestring import mark_safe

# Bestellung von nicht eingeloggten Usern
from . viewtools import gastCookie, gastBestellung

# zur Einbindung von Paypal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.

def shop(request):
    artikels = Artikel.objects.all()
    # Variable ctx für Rendering
    ctx = {'artikels':artikels}
    return render(request, 'shop/shop.html', ctx)

# Return-Wert Warenkorb für eingeloggte User aus der DB
# Klassendefinitionen dazu in models.py
def warenkorb(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        artikels = bestellung.bestellteartikel_set.all()

        # else betrifft die nicht eingeloggten User
        # die Artikeldaten wie Name, Bild und Preis werden auch aus der DB geladen 
    else:
        # artikels = []
        # bestellung = []

        # Kapitel 52
        # analoge Abfrage wird im Kassenblock benötigt
        # Kapitel 53
        # gesamter Block wird in viewtools.py ausgelagert, da er sich im artikelBackend wiederholt

        # try:
        #     warenkorb = json.loads(request.COOKIES['warenkorb'])
        # except:
        #     warenkorb = {}

        # artikels = []
        # bestellung = {'get_gesamtpreis':0, 'get_gesamtmenge':0}
        # # die Menge wird in einer eigenen Var abgespeichert
        # menge = bestellung['get_gesamtmenge']
        
        # for i in warenkorb:
        #     menge += warenkorb[i]["menge"]
        #     # Objekt Artikel holt Werte aus der DB, s. models.py
        #     artikel = Artikel.objects.get(id=i)
        #     gesamtpreis = (artikel.preis * warenkorb[i]['menge'])
        #     bestellung['get_gesamtpreis'] += gesamtpreis

        #     # artikel enthält ein Objekt artikel, das den Namen, die Bild-Url und den Preis enthält
        #     # menge und gesamtpreis kommen direkt aus artikel
        #     artikel = {
        #         'artikel':{
        #             'id':artikel.id,
        #             'name':artikel.name,
        #             'preis':artikel.preis,
        #             'bild':artikel.bild
        #         },
        #         'menge':warenkorb[i]['menge'],
        #         'get_summe':gesamtpreis
        #     }
        #     artikels.append(artikel)

        # nach Auslagerung des obigen Codes in die viewtools.py:
        cookieDaten = gastCookie(request)
        artikels = cookieDaten['artikels']
        bestellung = cookieDaten['bestellung']

    ctx = {"artikels":artikels, "bestellung":bestellung}        
    return render(request, 'shop/warenkorb.html',ctx)


# Return-Wert Kasse
def kasse(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        artikels = bestellung.bestellteartikel_set.all()
        
    # else gilt für nicht eingeloggte User
    # Werte werden aus dem Cookie warenkorb geholt bzw. über die artikel_id aus der DB
    else:
        # artikels = []
        # bestellung = []
        
        # Kapitel 53
        # gesamter Block wird in viewtools.py ausgelagert, da er sich im artikelBackend wiederholt
        cookieDaten = gastCookie(request)
        artikels = cookieDaten['artikels']
        bestellung = cookieDaten['bestellung']

    ctx = {"artikels":artikels, "bestellung":bestellung}      
    return render(request, 'shop/kasse.html', ctx)

# im artikelBackend werden Daten in die DB geladen oder geholt
def artikelBackend(request):
    daten = json.loads(request.body)
    artikelID = daten['artikelID']
    action = daten['action']
    # zum Testen
    # print('Artikel-ID: ', artikelID, ' Action: ', action)

    # kunde = request.user.kunde setzt einen eingeloggten Kunden voraus
    kunde = request.user.kunde
    artikel = Artikel.objects.get(id=artikelID)
    # wenn schon eine Bestellung existiert, "get", sonst "create"
    bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
    # falls derselbe Artikel schon im Warenkorb liegt, soll kein neuer kreiert werden, sondern hochgezaehlt werden
    bestellteArtikel, created = BestellteArtikel.objects.get_or_create(bestellung=bestellung, artikel=artikel)

    if action == 'bestellen':
        bestellteArtikel.menge = (bestellteArtikel.menge +1)

        # if führt zu Message
        # 5 Message-Typen: Debugging, Info, Success, Warning und Error
        # flash messages werden nur 1x aktibviert auf der Seite, wenn nicht noch einmal getriggert
        # Ausgabe dwer Messages in der index.html
        messages.success(request, "Artikel wurde zum Warenkorb hinzugefügt.")

    elif action == 'entfernen':
        bestellteArtikel.menge = (bestellteArtikel.menge -1)
        messages.warning(request, "Artikel wurde aus dem Warenkorb entfernt.")    

    bestellteArtikel.save()

    # wenn die Artikelanzahl auf 0 reduiziert wurde, dann Artikel aus Warenkorb entfernen
    if bestellteArtikel.menge <= 0:
        bestellteArtikel.delete()
    
    return JsonResponse("Artikel hinzugefügt", safe=False)

def loginBenutzer(request):
    seite = 'login'
    if request.method == 'POST':
        benutzername = request.POST['benutzername']
        passwort = request.POST['passwort']

        benutzer = authenticate(request, username=benutzername, password=passwort)

        if benutzer is not None:
            login(request, benutzer)
            return redirect('shop')
        else:
            messages.error(request, "Benutzername oder Passwort nicht korrekt.")

    return render(request, 'shop/login.html', {'seite': seite})

def logoutBenutzer(request):
    logout(request)
    return redirect('shop')


# Neukunden-Registrierung
# ein Neukunde wird als Benutzer, als Kunde und Inhaber einer Bestellung registriert
# er hat keinen Zugriff auf den admin-Bereich
def regBenutzer(request):
    seite = 'register'
    # form = UserCreationForm
    form = EigenesUserCreationForm

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = EigenesUserCreationForm(request.POST)
        if form.is_valid():
           benutzer = form.save(commit=False)
           benutzer.save()

           kunde = Kunde(name=request.POST['username'], benutzer=benutzer)
           kunde.save()
           bestellung = Bestellung(kunde=kunde)
           bestellung.save()

           login(request, benutzer)
           return redirect('shop')
        else:
            messages.error(request, "Fehlerhafte Eingabe!")

    ctx = {'form': form, 'seite': seite}
    return render(request, 'shop/login.html', ctx)


# Abschluss des Einkaufs (Warenkorb bezahlen)
def bestellen(request):
    # Kapitel 44
    # print(request.body)
    # messages.success(request, 'Vielen Dank für Ihre Bestellung.')
    # auftrags_id = uuid.uuid4()
    # daten = json.loads(request.body)
    # return zu obersten beiden Zeilen -> http://127.0.0.1:8000/bestellen/
    # Daten werden im Terminal ausgegeben
    # b'{"benutzerDaten":{"name":"Ceedee","email":"c.deten@gmx.de","gesamtpreis":"1534.98"},
    # "lieferadresse":{"adresse":"Holleweg 1","plz":"04277","stadt":"Leipzig","land":"D"}}'
    # [11/Jul/2023 23:49:57] "POST /bestellen/ HTTP/1.1" 200 24   
    # return JsonResponse('Bestellung erfolgreich', safe=False)


    # Kapitel 45
    # aus models.py kommen die Daten-Models zur Bestellung
    # zum Abschluss des Einkaufs muss die 'erledigt' auf '=True' gesetzt werden (default=False) 
    # -> Bestellung verschwindet damit aus dem Warenkorb

    # eindeutige Auftrags-ID
    auftrags_id = uuid.uuid4()
    daten = json.loads(request.body)

    # für eingeloggte Nutzer / Kunden
    # über Warenkorb.js und Backend aus Formular-Bereich der kasse.html
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
    # für nicht registrierte Nutzer
    else:
        # Test-Print -> abgelöst in Kapitel 54
        # print("nicht eingeloggt")        

        # Funktion ausgelagert in viewtools.py
        # Kapitel 54
        kunde, bestellung = gastBestellung(request, daten)       

    # Floatpreis für 2 Nachkommastellen
    gesamtpreis = float(daten['benutzerDaten']['gesamtpreis'])
    bestellung.auftrags_id = auftrags_id
    bestellung.erledigt = True
    bestellung.save()

    Adresse.objects.create(
        kunde=kunde,
        bestellung=bestellung,
        adresse=daten['lieferadresse']['adresse'],
        plz=daten['lieferadresse']['plz'],
        stadt=daten['lieferadresse']['stadt'],
        land=daten['lieferadresse']['land'],
    )
    
    # Bestellung mit Paypal-Zahlung abschließen
    # Code von Paypal-Seite (Doku): https://django-paypal.readthedocs.io/en/latest/standard/ipn.html
    # mit generiertem Test-Account 'business' -> live sollte hier die echte eMail stehen
    paypal_dict = {
    "business": "sb-qh5ij26259535@business.example.com",
    "amount": gesamtpreis,
    "item_name": "name of the item",
    # "invoice": "unique-invoice-id",
    "invoice": auftrags_id,
    
    # "currency" muss ergänzt werden
    "currency_code": "EUR",
    
    # "notify_url": Seite für die Paypal-Abwicklung
    "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    
    # "return": Erfolgsbestätigung nach Paypal-Abschluss 
    # -> reverse enthält die html-Page -> hier die Startseite -> kann beliebige andere sein
    "return": request.build_absolute_uri(reverse('shop')),
    # "cancel_return": nach Zahlungsabbruch
    "cancel_return": request.build_absolute_uri(reverse('shop')),
    
    # "custom": für eine benutzerdefinierte Seite im Zahlungsprozess
    }

    paypalform = PayPalPaymentsForm(initial=paypal_dict)
    
    auftragsUrl = str(auftrags_id)
    # Paypal-Form kann 1. hier aufgerufen werden oder 2. in HTML mit {{ paypalform }} + return render()
    messages.success(request, mark_safe("Vielen Dank für Ihre <a href='/bestellung/"+auftragsUrl+"'>Bestellung</a></br> Jetzt bezahlen: "+paypalform.render()))
    # zum Löschen des Cookies response in HttpResponse ändern -> Kapitel 54
    # return JsonResponse('Bestellung erfolgreich', safe=False)
    response = HttpResponse('Bestellung erfolgreich')
    response.delete_cookie('warenkorb')

    return response


# Bestellung -> bestellung.html
# wenn ein nicht eingeloggter User auf eine Bestell-Übersichts-Adresse eines Dritten zugreifen möchte, 
# -> soll er auf der Login-Seite landen
@login_required(login_url='login')
def bestellung(request,id):
    
    # Kapitel 46
    # id muss exakt der id aus der urls.py entsprechen
    # -> aus der DB wird genau ein Datensatz geladen
    # -> mit .get wird genau ein Datensatz der uuid geladen (eine Bestellung eines Kunden)
    # -> mit .filter wird ein Query-Set abgerufen
    # bestellung = Bestellung.objects.filter(auftrags_id=id)
    bestellung = Bestellung.objects.get(auftrags_id=id)

    # if-Abfrage soll die Bestellung aus dem Warenkorb UND den zugehörigen Kunden enthalten
    # -> Aufruf der Bestell-Übersicht ist damit auf diesen Kunden beschränkt
    if bestellung and str(request.user) == str(bestellung.kunde):
        bestellung = Bestellung.objects.get(auftrags_id=id)
        artikels = bestellung.bestellteartikel_set.all()
        ctx = {'artikels':artikels,'bestellung':bestellung}
        return render(request, 'shop/bestellung.html',ctx)
    else:
        # wenn die Bestellung nicht existiert, zurück zur Shop-Seite
        return redirect('shop')
    

# Fehlerbehandlung, wenn Seite nicht existiert
def fehler404(request, exception):
    return render(request, 'shop/404.html')
