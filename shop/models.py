from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# jedes neue Model muss mit python manage.py makemigrations für die Migration vorbereitet und 
# mit python manage.py migrate migriert werden
# -> vorher Server stoppen

class Kunde(models.Model):
    benutzer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    # E-Mail kann als Charfield oder als Emailfield deklariert werden
    # -> Emailfield ist ein Charfield mit Validator (Prüfung auf echte eMail-Ader.)
    # email = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

class Artikel(models.Model):
    name = models.CharField(max_length=200, null=True)
    beschreibung = models.TextField(null=True, blank=True)
    # für die Einrichtung als Gleitkommafeld kann FloatField oder Decimalfield genutzt werden
    # -> DecimalField erlaubt zusätzliche Attribute
    # -> max_digits bestimmt die max. Anzahl Ziffern vorm Komma -> 6 = max. 999.999
    # -> decimal_places bestimmmt die Anzahl Nachkommastellen -> 2 = ,00
    preis = models.DecimalField(max_digits=6, decimal_places=2)
    # pipenv install pillow
    bild = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    

class Bestellung(models.Model):
    kunde = models.ForeignKey(Kunde, on_delete=models.SET_NULL, null=True, blank=True)
    bestelldatum = models.DateTimeField(auto_now_add=True)
    erledigt = models.BooleanField(default=False, null=True, blank=True)
    auftrags_id = models.CharField(max_length=200, null=200)

    def __str__(self):
        return str(self.id)

    @property
    def get_gesamtpreis(self):
        bestellteartikels = self.bestellteartikel_set.all()
        gesamtpreis = sum(artikel.get_summe for artikel in bestellteartikels)
        return gesamtpreis

    @property
    def get_gesamtmenge(self):
        bestellteartikels = self.bestellteartikel_set.all()
        gesamtmenge = sum(artikel.menge for artikel in bestellteartikels)
        return gesamtmenge


class BestellteArtikel(models.Model):
    artikel = models.ForeignKey(Artikel, on_delete=models.SET_NULL, null=True, blank=True)
    bestellung = models.ForeignKey(Bestellung, on_delete=models.SET_NULL, null=True, blank=True)
    menge = models.IntegerField(default=0, null=True, blank=True)
    datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.artikel.name
    
    @property
    def get_summe(self):
        summe = self.artikel.preis * self.menge
        return summe

# Adresse kommt erst mit Kasse und Lieferung
class Adresse(models.Model):
    kunde = models.ForeignKey(Kunde, on_delete=models.SET_NULL, null=True, blank=True)
    bestellung = models.ForeignKey(Bestellung, on_delete=models.SET_NULL, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True)
    plz = models.CharField(max_length=200, null=True)
    stadt = models.CharField(max_length=200, null=True)
    land = models.CharField(max_length=200, null=True)
    datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.adresse)
    