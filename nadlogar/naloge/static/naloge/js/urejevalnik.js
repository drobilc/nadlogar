function ustvariNalogo(html) {
    let nalogaDiv = document.createElement('div');
    nalogaDiv.className = 'naloga';
    nalogaDiv.innerHTML = html;
    return nalogaDiv;
}

$(document).ready(function() {

    $('.orodna-vrstica .gumb').tooltip();

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

    // Dodaj poslusalce ob kliku na krizec, ki izbrisejo nalogo
    $(".uredi-nalogo").submit(function(event) {
        event.preventDefault();

        // Najdemo tip akcije, ki bi ga uporabnik rad izvedel
        let action = $(this).find("input[name='action']").val();

        // Ce zeli uporabnik urediti nalogo, mu prikazemo pojavno okno, kjer
        // lahko to stori.
        if (action === 'uredi_nalogo') {
            $('#uredi-nalogo-navodila').val($(this).find('input[name="naloga_navodila"]').val());
            $('#uredi-nalogo-popup').modal('show');
            return;
        }

        let serializedData = $(this).serialize();
        let url = $(this).attr('action');

        let naloga = $(this).closest('.naloga');

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