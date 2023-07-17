from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name ="shop"),

    # statische urls
    path('warenkorb/', views.warenkorb, name ="warenkorb"),
    path('kasse/', views.kasse, name ="kasse"),
    path('artikel_backend/', views.artikelBackend, name ="artikel_backend"),
    # Kunden-Login / -Logout
    # -> view sollte keine function login() oder logout() enthalten, da diese bereits existieren
    path('login/', views.loginBenutzer, name ="login"),
    path('logout/', views.logoutBenutzer, name ="logout"),
    # neuer Pfad für Registrierung neuer Nutzer
    path('register/', views.regBenutzer, name ="register"),
    # neuer Pfad für den Abschluss des Kaufs
    path('bestellen/', views.bestellen, name ="bestellen"),

    # Beisile für eine dynamische url 
    # -> <uuid:id> ist nicht statisch (mit Zahlen, Kleinbuchstaben und Bindestrichen)
    # -> andere Möglichkeiten: <str:id>, <int:id>, <slug:id>
    path('bestellung/<uuid:id>', views.bestellung, name ="bestellung"),
]
