function toggleNav() {
    var x = document.getElementById("navSmall");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

const fr = new FileReader();
function parseUploadedFile(input_id, info_id, callback) {
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert("Zdá se, že váš prohlížeč nepodporuje nutnou funkcionalitu.");
        return;
    }

    let input = document.getElementById(input_id);
    if (!input) {
        alert("Nepodařilo se najít vstupní element.<br>Kontaktujte, prosím, organizátory.");
    }
    else if (!input.files) {
        alert("Zdá se, že váš prohlížeč nepodporuje nutnou funkcionalitu (žádný načtený soubor).");
    }
    else if (!input.files[0]) {
        alert("Vyberte soubor předtím, než stisknete 'Nahrát'");
    }
    else {
        let file = input.files[0];
        fr.onload = function() {
            callback(fr.result, document.getElementById(info_id));
        }
        fr.readAsText(file);
    }
}
