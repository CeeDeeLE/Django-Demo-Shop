// zum User-Test -> nach logout Popup mit "AnonymousUser", sonst 'CeeDee'
// alert(benutzer);

// Warenkorb -> warenkorb.html
let bestellenButtons = document.getElementsByClassName("warenkorb-bestellen");

for (let i = 0; i < bestellenButtons.length; i++) {
  bestellenButtons[i].addEventListener("click", function () {
    let artikelID = this.dataset.artikel;
    let action = this.dataset.action;
    // alert("Aertikel-ID: " + artikelID + "  Action: " + action);

    if (benutzer == "AnonymousUser") {
      updateGastBestellung(artikelID, action);
    } else {
      updateKundenBestellung(artikelID, action);
    }
  });
}

// Bestellung von nicht registrierten Nutzern
function updateGastBestellung(artikelID, action) {
  //console.log("Gast " +artikelID+" "+action)
  if (action == "bestellen") {
    if (warenkorb[artikelID] == undefined) {
      warenkorb[artikelID] = { menge: 1 };
    } else {
      warenkorb[artikelID]["menge"] += 1;
    }
  }
  if (action == "entfernen") {
    warenkorb[artikelID]["menge"] -= 1;

    if (warenkorb[artikelID]["menge"] <= 0) {
      delete warenkorb[artikelID];
    }
  }
  document.cookie =
    "warenkorb=" +
    JSON.stringify(warenkorb) +
    ";domain;path=/; SameSite=None; Secure";
  console.log(warenkorb);
  location.reload();
}

// Bestellung von registrierten Nutzern / Kunden
function updateKundenBestellung(artikelID, action) {
  let url = "/artikel_backend/";

  fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ artikelID: artikelID, action: action }),
  }).then(() => location.reload());
}

// Kasse -> kasse.html
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
    // nach Eingabe Weiterleitung auf die Startseite
  }).then(() => (window.location.href = "/"));
}
