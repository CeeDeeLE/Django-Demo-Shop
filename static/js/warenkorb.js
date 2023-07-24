// zum User-Test -> nach logout Popup mit "AnonymousUser", sonst 'CeeDee'
// alert(benutzer);

// Warenkorb -> warenkorb.html
let bestellenButtons = document.getElementsByClassName("warenkorb-bestellen");

// alle Bestellen-Buttons werden in einer Schleife durchlaufen
for (let i = 0; i < bestellenButtons.length; i++) {
  bestellenButtons[i].addEventListener("click", function () {
    let artikelID = this.dataset.artikel;
    let action = this.dataset.action;
    // Testausgabe als Popup
    // alert("Aertikel-ID: " + artikelID + "  Action: " + action);

    // Funktionen bei Bestellung als nicht eingeloggter und als eingeloggter User folgen unten
    // benutzer-Variable wurde in der index.html als globale Variable angelegt
    // -> kann jetzt für eingeloggte und nicht eingeloggte User genutzt werden
    if (benutzer == "AnonymousUser") {
      updateGastBestellung(artikelID, action);
    } else {
      updateKundenBestellung(artikelID, action);
    }
  });
}

// Bestellung von nicht registrierten Nutzern
// Artikel-Nr. und Menge werden für den Gast statt in der DB im WK-Cookie gespeichert bzw. von dort gelöscht
function updateGastBestellung(artikelID, action) {
  // zum Testen Ausgabe in Console
  // console.log("Gast: Artikel-Nr.:" +artikelID+" Aktion: "+action)

  // Bestellung von eingeloggten Kunden wird an das Backend gesendet
  // -> s. views.py artikelBackend-View
  // wenn-dann wird für die Speicherung im warenkorb-Cookie (angelegt in der index.html)
  // -> für nicht eingeloggte User an dieser Stelle festgelegt, nicht in der views.py
  // -> ist aber analog zu artikelBackend
  if (action == "bestellen") {
    // wenn Artikel noch nicht im Warenkorb, dann mit Menge 1 hinzufügen
    if (warenkorb[artikelID] == undefined) {
      warenkorb[artikelID] = { menge: 1 };
    }
    // wenn der Artikel schon im Warenkorb, dann Menge +1
    else {
      warenkorb[artikelID]["menge"] += 1;
    }
  }
  // wenn Artikel im Warenkorb, dann bei Aktion "entfernen" -1
  if (action == "entfernen") {
    warenkorb[artikelID]["menge"] -= 1;

    // Löschen des Artikels aus dem Warenkorb, wenn Menge gleich Null
    if (warenkorb[artikelID]["menge"] <= 0) {
      delete warenkorb[artikelID];
    }
  }
  // Zeile aus index.html zum Anlegen des Cookies übernehmen
  // -> Cookie überschreiben
  document.cookie =
    "warenkorb=" +
    JSON.stringify(warenkorb) +
    ";domain;path=/; SameSite=None; Secure";
  // Test-Ausgabe in der Console
  console.log(warenkorb);
  // Artikel und Menge müssen für nicht eingeloggte User
  // -> noch der globalen context_processors.py bekannt gemacht werden
  // mit jeder Bestellung wird die Seite neu geladen, damit Artikel und Menge hochgezählt werden
  location.reload();
}

// Bestellung von registrierten Nutzern / Kunden -> Ansprache des Backends in views.py
function updateKundenBestellung(artikelID, action) {
  let url = "/artikel_backend/";

  // um Daten per Post an das Backend zu senden, wird ein CSFR-Tocken benötigt
  fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ artikelID: artikelID, action: action }),
  }).then(() => location.reload());
}

// Kasse
// -> kasse.html
let formular = document.getElementById("formular");
let gesamtpreis = document.getElementById("gesamtpreis").value;

formular.addEventListener("submit", function (e) {
  e.preventDefault();
  document.getElementById("formular-button").classList.add("d-none");
  document.getElementById("bezahlen-info").classList.remove("d-none");
});

document
  .getElementById("bezahlen-button")
  .addEventListener("click", function (e) {
    submitFormular();
  });

// Formulardaten an DB senden
function submitFormular() {
  // zum Testen Alert
  // alert("Bestellung aufgegeben.");

  let benutzerDaten = {
    // aus den Formularfeldern
    name: formular.inputName.value,
    email: formular.inputEmail.value,
    // aus hidden Feld im Formular -> ursprünglich aus views.py
    gesamtpreis: gesamtpreis,
  };
  let lieferadresse = {
    adresse: formular.inputAdresse.value,
    plz: formular.inputPlz.value,
    stadt: formular.inputStadt.value,
    land: formular.inputLand.value,
  };
  // zum Testen Consolen-Ausgabe -> unteren Teil deaktivieren
  console.log(benutzerDaten, lieferadresse);

  // Datenverarbeitung nach Bezahlen
  // Formulardaten werden an das Backend gesendet und in der bestellen-URL verarbeitet
  // -> s. views.py / bestellen
  let url = "/bestellen/";

  fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      benutzerDaten: benutzerDaten,
      lieferadresse: lieferadresse,
    }),
    // nach Absenden Weiterleitung auf die Startseite
  }).then(() => (window.location.href = "/"));
}
