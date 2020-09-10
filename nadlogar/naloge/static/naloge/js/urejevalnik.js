// Katero nalogo uporabnik trenutno ureja
var trenutnaNaloga = null;

function ustvariNalogo(html) {
    let nalogaDiv = document.createElement('div');
    nalogaDiv.className = 'naloga';
    nalogaDiv.innerHTML = html;
    return nalogaDiv;
}

$(document).ready(function() {

    $('.orodna-vrstica .gumb').tooltip();

    $('#vrsta-naloge').change(function(event) {
        if (typeof NAVODILA === "undefined")
            return;
        
        let selectedElement = $(this).val();
        if (NAVODILA.hasOwnProperty(selectedElement)) {
            $('#navodila').val(NAVODILA[selectedElement]);
        } else {
            $('#navodila').val('');
        }
    });

    $('#orodna-vrstica button').each(function() {
        $(this).click(function(event) {
            // Ce uporabnik klikne na enega izmed gumbov v orodni vrstici,
            // najprej prekinemo posiljanje forme
            event.preventDefault();
            let forma = $(this).closest('form');

            // Nato najdemo nevidno vnosno polje z imenom action in mu
            // nastavimo vrednost na vrednost gumba
            forma.find("input[name='action']").val($(this).val());

            // Dejansko posljemo formo
            forma.submit();
        });
    });

    $('#uredi-nalogo').submit(function(event) {
        event.preventDefault();
        let serializedData = $(this).serialize();
        let url = $(this).attr('action');
        $.ajax({
            type : 'POST',
            url :  url,
            data : serializedData,
            success : function(response) {
                trenutnaNaloga.find('.primeri').html(response);
                $('#uredi-nalogo-popup').modal('hide');
            },
            error : function(response) {
                console.log(response)
            }
        });
    });

    // Dodaj poslusalce ob kliku na krizec, ki izbrisejo nalogo
    $(".uredi-nalogo").submit(function(event) {
        event.preventDefault();

        // Najdemo tip akcije, ki bi ga uporabnik rad izvedel
        let action = $(this).find("input[name='action']").val();

        let naloga = $(this).closest('.naloga');

        // Ce zeli uporabnik urediti nalogo, mu prikazemo pojavno okno, kjer
        // lahko to stori.
        if (action === 'uredi_nalogo') {
            // Vsaka naloga vsebuje se obrazec za spreminjanje podatkov naloge.
            // Obrazec kopiramo v formo znotraj pojavnega okna.
            $('#uredi-nalogo-form').html(naloga.find('.uredi-nalogo-obrazec').html());
            $('#uredi-nalogo-popup').modal('show');
            trenutnaNaloga = naloga;
            return;
        }

        let serializedData = $(this).serialize();
        let url = $(this).attr('action');

        // Skrijemo VSE tooltipe na strani
        $('[data-toggle="tooltip"]').tooltip('hide');

        if (action === 'odstrani_nalogo') {
            // Odstranimo nalogo iz seznama nalog
            naloga.remove();
        } else if (action === 'premakni_gor') {
            // Najdemo prejsnjo nalogo in ju zamenjamo
            let prejsnjaNaloga = naloga.prev();
            if (prejsnjaNaloga) {
                prejsnjaNaloga.before(naloga);
            }
        } else if (action === 'premakni_dol') {
            // Najdemo naslednjo nalogo in ju zamenjamo
            let naslednjaNaloga = naloga.next();
            if (naslednjaNaloga) {
                naloga.before(naslednjaNaloga);
            }
        }

        $.ajax({
            type : 'POST',
            url :  url,
            data : serializedData,
            success : function(response) {
                if (action === 'ponovno_generiraj') {
                    // Popravimo vsebino naloge
                    naloga.find('.primeri').html(response);
                } else if (action === 'dodaj_primer') {
                    naloga.find('.primeri').html(response);
                }
            },
            error : function(response) {
                console.log(response)
            }
        });
        
    });

    $("#naloga-form").submit(function(event) {
        event.preventDefault();
        
        var serializedData = $(this).serialize();
        let url = $(this).attr('action');

        $.ajax({
            type : 'POST',
            url :  url,
            data : serializedData,
            success : function(response) {
                // Ustvari novo vsebnik z nalogo in ga dodaj na stran
                let novaNaloga = ustvariNalogo(response);
                document.getElementById("naloge").appendChild(novaNaloga);

                // Ponastavi obrazec za dodajanje naloge
                $("#naloga-form")[0].reset();

                // Zapri pojavno okno za dodajanje naloge
                $('#dodaj-nalogo-popup').modal('hide');

                // Scollaj do novo dodanega elementa
                novaNaloga.scrollIntoView({ behavior: 'smooth' });
            },
            error : function(response) {
                console.log(response)
            }
        });
    });
});