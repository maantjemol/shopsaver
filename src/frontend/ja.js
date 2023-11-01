document.write("this is a JS code");
// Zoekfunctie
function zoek() {
    var zoekwoord = document.getElementById("search-input").value;
    // Simuleer hier een zoekopdracht (vervang dit met je eigen zoeklogica)
    var zoekresultaten = ["Resultaat 1", "Resultaat 2", "Resultaat 3"];
    
    var zoekresultatenContainer = document.getElementById("search-results");
    zoekresultatenContainer.innerHTML = ""; // Leeg de zoekresultaten container

    for (var i = 0; i < zoekresultaten.length; i++) {
        var resultaat = document.createElement("div");
        resultaat.textContent = zoekresultaten[i];
        zoekresultatenContainer.appendChild(resultaat);
    }
}

// Voeg een klikgebeurtenis toe aan de zoekknop
var zoekKnop = document.getElementById("search-button");
zoekKnop.addEventListener("click", zoek);